"""Telegram Maintenance - Purge old Data Manager."""
from __future__ import annotations

import logging
import os.path
from configparser import ConfigParser
from typing import Dict, List, cast

from TEx.core.base_module import BaseModule
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMediaDatabaseManager, TelegramMessageDatabaseManager
from TEx.models.database.telegram_db_model import TelegramGroupOrmEntity, TelegramMediaOrmEntity

logger = logging.getLogger('TelegramExplorer')


class TelegramMaintenancePurgeOldData(BaseModule):
    """Telegram Maintenance - Purge old Data Manager."""

    async def can_activate(self, config: ConfigParser, args: Dict, data: Dict) -> bool:
        """
        Abstract Method for Module Activation Function.

        :return:
        """
        return cast(bool, args['purge_old_data'])

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not await self.can_activate(config, args, data):
            logger.debug('\t\tModule is Not Enabled...')
            return

        # Load Groups from DB
        groups: List[TelegramGroupOrmEntity] = TelegramGroupDatabaseManager.get_all_by_phone_number(
            config['CONFIGURATION']['phone_number'])
        logger.info(f'\t\tFound {len(groups)} Groups')

        for group in groups:
            try:
                await self.__process_group(
                    group_id=group.id,
                    group_name=group.title,
                    max_age=int(args['limit_days']),
                    media_root_path=config['CONFIGURATION']['data_path'],
                    )
            except ValueError as ex:
                logger.info('\t\t\tUnable to Purge Old Messages...')
                logger.error(ex)

        # Compress DB
        TelegramMediaDatabaseManager.apply_db_maintenance()
        logger.info('\t\t\tDB Optimized Successfully')

    async def __process_group(self, group_id: int, group_name: str, max_age: int, media_root_path: str) -> None:
        """Process and Remove Old Messages and Medias from a Single Group."""
        logger.info(f'\t\tPurging ({group_id}) "{group_name}"')

        # Get all Old Medias
        all_medias: List[TelegramMediaOrmEntity] = TelegramMediaDatabaseManager.get_all_medias_by_age(
            group_id=group_id,
            media_limit_days=max_age,
            )
        media_count: int = len(all_medias)
        logger.info(f'\t\t\t{len(all_medias)} Medias to be Removed')

        if media_count > 0:

            for media in all_medias:

                # Remove from Disk
                media_file_name: str = os.path.join(media_root_path, 'media', str(media.group_id), media.file_name)
                logger.info(f'\t\t\t\t{media_file_name}')

                if os.path.exists(media_file_name):
                    os.remove(media_file_name)

                # Remove from DB
                TelegramMediaDatabaseManager.delete_media_by_id(media_id=media.id)

        # Delete all Old Messages
        total_messages: int = TelegramMessageDatabaseManager.remove_all_messages_by_age(
            group_id=group_id,
            limit_days=max_age,
            )
        logger.info(f'\t\t\t{total_messages} Messages Removed')
