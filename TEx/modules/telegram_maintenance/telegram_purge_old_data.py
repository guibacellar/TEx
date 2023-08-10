"""Telegram Maintenance - Purge old Data Manager."""
import logging
from configparser import ConfigParser
from typing import Dict, List

from TEx.core.base_module import BaseModule
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMediaDatabaseManager, \
    TelegramMessageDatabaseManager
from TEx.models.database.telegram_db_model import TelegramGroupOrmEntity

logger = logging.getLogger()


class TelegramMaintenancePurgeOldData(BaseModule):
    """Telegram Maintenance - Purge old Data Manager."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not args['purge_old_data']:
            logger.info('\t\tModule is Not Enabled...')
            return

        # Load Groups from DB
        groups: List[TelegramGroupOrmEntity] = TelegramGroupDatabaseManager.get_all_by_phone_number(
            config['CONFIGURATION']['target_phone_number'])
        logger.info(f'\t\tFound {len(groups)} Groups')

        for group in groups:
            try:
                await self.__process_group(
                    group_id=group.id,
                    group_name=group.title,
                    max_age=int(args['limit_days'])
                    )
            except ValueError as ex:
                logger.info('\t\t\tUnable to Purge Old Messages...')
                logger.error(ex)

    async def __process_group(self, group_id: int, group_name: str, max_age: int) -> None:
        """Process and Remove Old Messages and Medias from a Single Group."""
        logger.info(f'\t\tPurging ({group_id}) "{group_name}"')

        # Delete all Old Medias
        total_media: int = TelegramMediaDatabaseManager.remove_all_medias_by_age(
            group_id=group_id,
            media_limit_days=max_age
            )
        logger.info(f'\t\t\t{total_media} Medias Removed')

        # Compress DB
        TelegramMediaDatabaseManager.apply_db_maintenance()
        logger.info('\t\t\tDB Optimized Successfully')

        # Delete all Old Messages
        total_messages: int = TelegramMessageDatabaseManager.remove_all_messages_by_age(
            group_id=group_id,
            limit_days=max_age
            )
        logger.info(f'\t\t\t{total_messages} Messages Removed')
