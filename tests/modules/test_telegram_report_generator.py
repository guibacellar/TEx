"""Telegram Groups Scrapper Tests."""

import asyncio
import datetime
import shutil
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock

import pytz
from sqlalchemy import select, insert, delete
from telethon.tl.functions.messages import GetDialogsRequest

from TEx.core.dir_manager import DirectoryManagerUtils
from TEx.database.db_initializer import DbInitializer
from TEx.database.db_manager import DbManager
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMessageDatabaseManager
from TEx.models.database.telegram_db_model import (
    TelegramGroupOrmEntity,
    TelegramMediaOrmEntity, TelegramMessageOrmEntity, TelegramUserOrmEntity,
)
from TEx.modules.telegram_messages_scrapper import TelegramGroupMessageScrapper
from TEx.modules.telegram_report_generator import TelegramReportGenerator
from tests.modules.mockups_groups_mockup_data import base_groups_mockup_data, base_messages_mockup_data, \
    base_users_mockup_data


class TelegramGroupMessageScrapperTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('../../config.ini')

        DirectoryManagerUtils.ensure_dir_struct('_data')
        DirectoryManagerUtils.ensure_dir_struct('_data/resources')
        DirectoryManagerUtils.ensure_dir_struct('_data/media')

        DbInitializer.init(data_path='_data/', args={})

        # Reset SQLlite Groups
        DbManager.SESSIONS['data'].execute(delete(TelegramMessageOrmEntity))
        DbManager.SESSIONS['data'].execute(delete(TelegramGroupOrmEntity))
        DbManager.SESSIONS['data'].commit()

        # Add Group 1 - Without Any Message
        TelegramGroupDatabaseManager.insert_or_update({
            'id': 1, 'constructor_id': 'A', 'access_hash': 'AAAAAA',
            'fake': False, 'gigagroup': False, 'has_geo': False,
            'participants_count': 1, 'restricted': False,
            'scam': False, 'group_username': 'UN-A',
            'verified': False, 'title': 'UT-01', 'source': 'UT-PHONE'
        })

        # Add Group 2 - With Previous Messages
        TelegramGroupDatabaseManager.insert_or_update({
            'id': 2, 'constructor_id': 'B', 'access_hash': 'BBBBBB',
            'fake': False, 'gigagroup': False, 'has_geo': False,
            'participants_count': 2, 'restricted': False,
            'scam': False, 'group_username': 'UN-b',
            'verified': False, 'title': 'UT-02', 'source': 'UT-PHONE'
        })
        TelegramMessageDatabaseManager.insert({
            'id': 55, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 1', 'raw': 'Raw Message 1', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': None
        })

        # Initialize the Medias Groups
        DbInitializer.init_media_dbs(data_path='_data/', args={'target_phone_number': 'UT-PHONE'})

        # Cleanup Media DBs
        DbManager.SESSIONS['media_1'].execute(delete(TelegramMediaOrmEntity))
        DbManager.SESSIONS['media_2'].execute(delete(TelegramMediaOrmEntity))
        DbManager.SESSIONS['data'].commit()

    def tearDown(self) -> None:
        DbManager.SESSIONS['media_1'].close()
        DbManager.SESSIONS['media_2'].close()
        DbManager.SESSIONS['data'].close()

    def test_run_generate_report(self):
        """Test Run Method for Scrap Telegram Groups."""

        # Call Test Target Method
        target: TelegramReportGenerator = TelegramReportGenerator()
        args: Dict = {
            'target_phone_number': 'UT-PHONE',  # TODO: Make a new Test when the target_phone_number has no Groups
            'data_path': '_data',
            'report_folder': '_report',
            'group_id': '*',
            'order_desc': True,
            'filter': None,
            'limit_days': 30,
            'report': True
        }
        data: Dict = {}

        with self.assertLogs() as captured:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                target.run(
                    config=self.config,
                    args=args,
                    data=data
                )
            )

            # # Check Logs
            # self.assertEqual(9, len(captured.records))
            # self.assertEqual('		Found 2 Groups', captured.records[0].message)
            # self.assertEqual('		Download Messages from "UT-01" > Last Offset: None', captured.records[1].message)
            # self.assertEqual('			Downloading Photo from Message 183018', captured.records[2].message)
            # self.assertEqual('			Downloading Media from Message 183644 (12761.9 Kbytes) as application/vnd.android.package-archive', captured.records[3].message)
            # self.assertEqual('			Downloading Media from Message 183659 (58.8613 Kbytes) as image/webp', captured.records[4].message)
            # self.assertEqual('			Downloading Media from Message 183771 (2258.64 Kbytes) as video/mp4', captured.records[5].message)
            # self.assertEqual('			Downloading Media from Message 192 (20.1279 Kbytes) as application/x-tgsticker', captured.records[6].message)
            # self.assertEqual('		Download Messages from "UT-01" > Last Offset: 183771', captured.records[7].message)
            # self.assertEqual('		Download Messages from "UT-02" > Last Offset: 55', captured.records[8].message)
