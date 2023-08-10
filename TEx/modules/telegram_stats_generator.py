"""Telegram Statistics Generator."""
import datetime
import logging
import os
import shutil
from configparser import ConfigParser
from io import TextIOWrapper
from typing import Dict, List, TypedDict

import pytz

from TEx.core.base_module import BaseModule
from TEx.core.dir_manager import DirectoryManagerUtils
from TEx.database.telegram_group_database import (
    TelegramGroupDatabaseManager,
    TelegramMediaDatabaseManager, TelegramMessageDatabaseManager
    )
from TEx.models.database.telegram_db_model import (
    TelegramGroupOrmEntity
    )
from TEx.models.facade.telegram_group_report_facade_entity import TelegramGroupReportFacadeEntity, \
    TelegramGroupReportFacadeEntityMapper

logger = logging.getLogger()


class TelegramStatsGenerator(BaseModule):
    """Statistics Generator."""

    class RenderParams(TypedDict):
        """Render Method TypeHint."""

        limit_seconds: int
        report_root_folder: str
        stats_total_messages: int
        stats_messages_per_groups: List[Dict]
        stats_total_groups: int
        stats_total_active_users: int
        target_phone_number: str

    __USERS_RESOLUTION_CACHE: Dict = {}

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not args['stats']:
            logger.info('\t\tModule is Not Enabled...')
            return

        # Check Report and Assets Folder
        report_root_folder: str = args['report_folder']

        # Purge Report Folder
        if os.path.exists(report_root_folder):
            shutil.rmtree(report_root_folder)

        # Create Dir Structure
        DirectoryManagerUtils.ensure_dir_struct(report_root_folder)

        # Statistics
        stats_total_groups: int = 0
        stats_total_messages: int = 0
        stats_total_active_users: int = 0
        stats_messages_per_groups: List[Dict] = []

        # Compute Date/Time Limits
        limit_seconds: int = int(args['limit_days']) * 24 * 60 * 60

        # Load Groups
        groups: List[TelegramGroupReportFacadeEntity] = await self.__load_groups(config=config)
        logger.info(f'\t\tFound {len(groups)} Groups')
        stats_total_groups += len(groups)

        # Get Stats from Each Group
        for group in groups:

            logger.info(f'\t\t\tCounting for {group.id}')
            h_result: Dict = await self.__get_group_stats(group=group, limit_seconds=limit_seconds)

            stats_total_messages += h_result['messages']
            stats_messages_per_groups.append(h_result)

        # Count All Active Users
        stats_total_active_users = TelegramMessageDatabaseManager.count_active_users(message_datetime_limit_seconds=limit_seconds)

        # Draw
        await self.__render(
            {
                'target_phone_number': config['CONFIGURATION']['phone_number'],
                'report_root_folder': report_root_folder,
                'limit_seconds': limit_seconds,
                'stats_total_messages': stats_total_messages,
                'stats_messages_per_groups': stats_messages_per_groups,
                'stats_total_groups': stats_total_groups,
                'stats_total_active_users': stats_total_active_users
                })

    async def __load_groups(self, config: ConfigParser) -> List[TelegramGroupReportFacadeEntity]:
        """
        Load Groups.

        :param args: Input Args
        :return: Groups List
        """
        db_groups: List[TelegramGroupOrmEntity] = TelegramGroupDatabaseManager.get_all_by_phone_number(config['CONFIGURATION']['phone_number'])
        db_groups.sort(key=lambda group: group.group_username if group.group_username is not None else '')

        # Map to Facade Entities
        groups: List[TelegramGroupReportFacadeEntity] = [
            TelegramGroupReportFacadeEntityMapper.create_from_dbentity(item)
            for item in db_groups
            ]

        return groups

    async def __render_media_stats(self, file: TextIOWrapper, max_large_group_name: int, stats_messages_per_groups: List[Dict]) -> None:
        """Render Media Statistics."""
        file.write('\n\n**** Media Statistics for Groups ****')
        for single in stats_messages_per_groups:
            if not single['media'] or single['media'] == {}:
                continue

            file.write(f'\n{single["group"].ljust(max_large_group_name)}')

            for mimetype, stats in single['media'].items():
                ct_media_count: str = f'{stats["count"]} entries'
                ct_media_size_bytes: str = f'{stats["size_bytes"]} bytes'
                ct_media_size_mbytes: str = f'{(stats["size_bytes"] / 1024 / 1024):.2f} mbytes'

                file.write(
                    f'\n\t{mimetype.ljust(70)}: {ct_media_count.ljust(16)}: {ct_media_size_bytes} ({ct_media_size_mbytes})')
            file.write('\n')

    async def __render_messages_stats(self, file: TextIOWrapper, max_large_group_name: int, stats_messages_per_groups: List[Dict]) -> None:
        """Render Messages Statistics."""
        file.write('\n\n**** Messages Statistics for Groups ****')
        for single in stats_messages_per_groups:
            ct_group_name: str = single["group"]
            ct_total_messages: str = f'{single["messages"]} messages'
            ct_active_users: str = f'{single["active_users"]} active users'

            file.write(
                f'\n{ct_group_name.ljust(max_large_group_name)}: {ct_total_messages.ljust(16)}: {ct_active_users}')

    async def __get_group_stats(self, group: TelegramGroupReportFacadeEntity, limit_seconds: int) -> Dict:
        """
        Get a Single Group Stats.

        :param group: Group Entity
        :param group: Total Limit Seconds
        :return:
        """
        # Count Messages
        message_count: int = TelegramMessageDatabaseManager.count_messages_from_group(
            group_id=group.id,
            message_datetime_limit_seconds=limit_seconds
            )

        # Count Active Users
        active_user_count: int = TelegramMessageDatabaseManager.count_active_users_from_group(
            group_id=group.id,
            message_datetime_limit_seconds=limit_seconds
            )

        # Count Media
        media_stats: Dict = TelegramMediaDatabaseManager.stats_all_medias_from_group_by_mimetype(
            group_id=group.id,
            file_datetime_limit_seconds=limit_seconds
            )

        return {
            'group': f'{group.group_username}_{group.id}',
            'messages': message_count,
            'active_users': active_user_count,
            'media': media_stats
            }

    async def __render(self, params: RenderParams) -> None:
        """Render Report."""
        # Calculate Average Messages per Day
        stats_avg_messages_day = params['stats_total_messages'] / datetime.timedelta(seconds=params['limit_seconds']).days

        # Define the Largest Group Name
        max_large_group_name: int = max([len(item['group']) for item in params['stats_messages_per_groups']]) + 1  # pylint: disable=R1728

        logger.info('\t\t\tRendering')
        with open(f'{params["report_root_folder"]}/stats.txt', 'wt', encoding='utf-8') as file:

            # Compute Report Period
            end = datetime.datetime.now(tz=pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
            start = (datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(seconds=params['limit_seconds'])).strftime('%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now(tz=pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')

            file.write(f'TEx Statistics Report ({params["target_phone_number"]})')
            file.write(f'\nGenerated at {now} for period starting from {start} to {end}\n')

            file.write(f'\nTotal Groups      : {params["stats_total_groups"]}')
            file.write(f'\nTotal Messages    : {params["stats_total_messages"]} (~ {stats_avg_messages_day:.0f}/day)')
            file.write(f'\nTotal Active Users: {params["stats_total_active_users"]}')

            await self.__render_messages_stats(file, max_large_group_name, params['stats_messages_per_groups'])
            await self.__render_media_stats(file, max_large_group_name, params['stats_messages_per_groups'])

            file.flush()
            file.close()
