"""Telegram Report Generator."""
import base64
import hashlib
import logging
import os
import shutil
from configparser import ConfigParser
from operator import attrgetter
from typing import Dict, List

from sqlalchemy.engine import ChunkedIteratorResult

from TEx.core.base_module import BaseModule
from TEx.core.dir_manager import DirectoryManagerUtils
from TEx.database.telegram_group_database import (
    TelegramGroupDatabaseManager,
    TelegramMediaDatabaseManager
    )
from TEx.models.database.telegram_db_model import (
    TelegramGroupOrmEntity
    )
from TEx.models.facade.telegram_group_report_facade_entity import TelegramGroupReportFacadeEntity, \
    TelegramGroupReportFacadeEntityMapper

logger = logging.getLogger()


class TelegramExportFileGenerator(BaseModule):
    """Export Telegram Files."""

    __USERS_RESOLUTION_CACHE: Dict = {}
    __HASH_CACHE: List[str] = []

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not args['export_file']:
            logger.info('\t\tModule is Not Enabled...')
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
            args['target_phone_number'])
        logger.info(f'\t\tFound {len(db_groups)} Groups')

        # Map to Facade Entities
        groups: List[TelegramGroupReportFacadeEntity] = [
            TelegramGroupReportFacadeEntityMapper.create_from_dbentity(item)
            for item in db_groups
            ]

        # Filter Groups
        groups = self.__filter_groups(
            args=args,
            source=groups
            )

        # Process Each Group
        for group in groups:
            logger.info(f'\t\tProcessing "{group.title}" ({group.id})')
            await self.__export_data(
                args=args,
                group=group,
                report_root_folder=report_root_folder
                )

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
        # Get Medias
        logger.info('\t\t\tRetrieving Messages')

        # Apply Date/Time Limits
        limit_days: int = int(args['limit_days'])
        limit_seconds: int = limit_days * 24 * 60 * 60

        # Get Filter Expression
        filter_by_filename: List[str] = args['filter'].split(',') if args['filter'] != '*' else []

        # Get Medias
        logger.info('\t\t\tLoading Medias')
        medias: ChunkedIteratorResult = TelegramMediaDatabaseManager.get_all_medias_from_group_and_mimetype(
            group_id=group.id,
            file_datetime_limit_seconds=limit_seconds,
            mime_type=args['mime_type'],
            file_name_part=filter_by_filename
            )

        # if Has 0 Messages, Get Out
        for media in medias.yield_per(1):

            # Calculate Filename
            file_name: str = f'G_{group.id}_MID_{media[0].id}_' + "".join(char for char in media[0].file_name if char not in "%:/,\\\n\t\r[]<>*?;")

            # Get Binary Content
            bin_content = base64.b64decode(media[0].b64_content)

            # Compute FileHash
            f_hash: str = hashlib.md5(bin_content).hexdigest()  # nosec

            # Check if Hash alread Exists in this Session
            if f_hash in TelegramExportFileGenerator.__HASH_CACHE:
                logger.info(f'\t\t\tFile Already Write - Same Hash - ({file_name}) > ID: {media[0].id} at {media[0].date_time}')
                continue

            # Write
            logger.info(f'\t\t\tWriting - ({file_name}) > ID: {media[0].id} at {media[0].date_time}')

            with open(os.path.join(report_root_folder, file_name), 'wb') as file:
                file.write(bin_content)
                file.flush()
                file.close()

            # Update Hash Table
            TelegramExportFileGenerator.__HASH_CACHE.append(f_hash)
