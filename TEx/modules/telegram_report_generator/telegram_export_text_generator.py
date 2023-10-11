"""Telegram Report Generator."""
from __future__ import annotations

import logging
import os
import re
import shutil
from configparser import ConfigParser
from operator import attrgetter
from typing import Dict, List, Optional, cast

import aiofiles

from TEx.core.base_module import BaseModule
from TEx.core.dir_manager import DirectoryManagerUtils
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMessageDatabaseManager
from TEx.models.database.telegram_db_model import TelegramGroupOrmEntity, TelegramMessageOrmEntity
from TEx.models.facade.telegram_group_report_facade_entity import TelegramGroupReportFacadeEntity, TelegramGroupReportFacadeEntityMapper
from TEx.models.facade.telegram_message_report_facade_entity import TelegramMessageReportFacadeEntity, TelegramMessageReportFacadeEntityMapper

logger = logging.getLogger('TelegramExplorer')


class TelegramExportTextGenerator(BaseModule):
    """Export Telegram Messages."""

    __USERS_RESOLUTION_CACHE: Dict = {}

    async def can_activate(self, config: ConfigParser, args: Dict, data: Dict) -> bool:
        """
        Abstract Method for Module Activation Function.

        :return:
        """
        return cast(bool, args['export_text'])

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not await self.can_activate(config, args, data):
            logger.debug('\t\tModule is Not Enabled...')
            return

        # Check Report and Assets Folder
        report_root_folder: str = args['report_folder']
        assets_root_folder: str = f'{report_root_folder}/assets/'

        # Purge Report Folder
        if os.path.exists(report_root_folder):
            shutil.rmtree(report_root_folder)

        # Create Dir Structure
        DirectoryManagerUtils.ensure_dir_struct(report_root_folder)
        DirectoryManagerUtils.ensure_dir_struct(assets_root_folder)

        # Load Groups from DB
        db_groups: List[TelegramGroupOrmEntity] = TelegramGroupDatabaseManager.get_all_by_phone_number(
            config['CONFIGURATION']['phone_number'])
        logger.info(f'\t\tFound {len(db_groups)} Groups')

        # Map to Facade Entities
        groups: List[TelegramGroupReportFacadeEntity] = [
            TelegramGroupReportFacadeEntityMapper.create_from_dbentity(item)
            for item in db_groups
            ]

        # Filter Groups
        groups = self.__filter_groups(
            args=args,
            source=groups,
            )

        # Process Each Group
        try:
            for group in groups:
                logger.info(f'\t\tProcessing "{group.title}" ({group.id})')
                await self.__export_data(
                    args=args,
                    group=group,
                    report_root_folder=report_root_folder,
                    )
        except re.error as _ex:
            logger.warning(msg=f'\t\tInvalid RegEx: "{str(_ex.msg)}" - Pattern: {str(_ex.pattern)}')
            data['internals']['panic'] = True

    def __filter_groups(self, args: Dict, source: List[TelegramGroupReportFacadeEntity]) -> List[TelegramGroupReportFacadeEntity]:
        """Apply Filter on Gropus."""
        groups: List[TelegramGroupReportFacadeEntity] = []

        # Filter Groups
        if args['group_id'] != '*':
            target_group_ids: List = [int(group) for group in str(args['group_id']).split(',')]
            logger.info(f'\t\tFiltering Groups by {target_group_ids}')
            groups = list(filter(lambda x: len([tg for tg in target_group_ids if tg == x.id]) > 0, source))
            logger.info(f'\t\tFound {len(groups)} after filtering')

        else:
            groups.extend(source)

        # Sort Groups by Title
        return sorted(groups, key=attrgetter('title'))

    async def __export_data(self, args: Dict, group: TelegramGroupReportFacadeEntity, report_root_folder: str) -> None:
        """Process the Export for a Single Group Chat."""
        # Download All Messages
        logger.info('\t\t\tRetrieving Messages')

        # Apply Date/Time Limits
        limit_days: int = int(args['limit_days'])
        limit_seconds: int = limit_days * 24 * 60 * 60

        db_messages: List[TelegramMessageOrmEntity] = TelegramMessageDatabaseManager.get_all_messages_from_group(
            group_id=group.id,
            order_by_desc=args['order_desc'],
            message_datetime_limit_seconds=limit_seconds,
            )

        # Convert Messages to Report Facade Entity
        messages: List[TelegramMessageReportFacadeEntity] = [
            TelegramMessageReportFacadeEntityMapper.create_from_dbentity(item)
            for item in db_messages
            ]

        # Filter Messages
        logger.info('\t\t\tFiltering')
        filter_regex: Optional[str] = args['regex'] if args['regex'] else None
        filtered_messages: List[str] = self.filter_messages(messages=messages, filter_regex=filter_regex)

        # if Has 0 Messages, Get Out
        if len(filtered_messages) == 0:
            return

        # Dedup Messages
        filtered_messages = list(dict.fromkeys(filtered_messages))

        logger.info('\t\t\tRendering')
        async with aiofiles.open(f'{report_root_folder}/result_{group.group_username}_{group.id}.txt', 'wb') as file:

            for message in filtered_messages:
                if isinstance(message, str):
                    await file.write(message.encode('utf-8'))
                    await file.write(b'\r\n')

            await file.flush()
            await file.close()

        # Add Meta in Group
        group.meta_message_count = len(filtered_messages)

    def filter_messages(self, messages: List[TelegramMessageReportFacadeEntity], filter_regex: Optional[str]) -> List[str]:
        """Filter Messages."""
        if not filter_regex or len(filter_regex) == 0:
            return [item.raw for item in messages]

        h_messages: List[str] = []

        # Compile Regex
        compiled_regex = re.compile(filter_regex, flags=re.IGNORECASE | re.MULTILINE)

        # Loop on Messages
        for message in messages:

            # Process Each Filter
            matches = compiled_regex.findall(message.raw)

            if len(matches) > 0:
                for match in matches:
                    if isinstance(match, str):
                        h_messages.append(match)
                    elif isinstance(match, tuple):
                        h_messages.extend(list(match))

        return h_messages

    def ireplace(self, old: str, repl: str, text: str) -> str:
        """Case Insensitive Replace."""
        return re.sub('(?i)' + re.escape(old), lambda _m: repl, text)
