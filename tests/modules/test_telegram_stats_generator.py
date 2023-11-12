"""Telegram Staus Generator List Tests."""

import asyncio
import os.path
import unittest
from configparser import ConfigParser
import datetime
from typing import Dict

import pytz

from TEx.database import GROUPS_CACHE, USERS_CACHE
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMediaDatabaseManager, \
    TelegramMessageDatabaseManager, \
    TelegramUserDatabaseManager
from TEx.modules.telegram_stats_generator import TelegramStatsGenerator
from tests.modules.common import TestsCommon
from tests.modules.mockups_groups_mockup_data import base_users_mockup_data


class TelegramStatsGeneratorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

        TestsCommon.basic_test_setup()
        GROUPS_CACHE.clear()
        USERS_CACHE.clear()

        # Add Users
        TelegramUserDatabaseManager.insert_or_update({
            'id': 1, 'is_bot': False, 'is_fake': False, 'is_self': False, 'is_scam': False, 'is_verified': False
        })

        TelegramUserDatabaseManager.insert_or_update({
            'id': 2, 'is_bot': False, 'is_fake': False, 'is_self': False, 'is_scam': False, 'is_verified': False
        })

        TelegramUserDatabaseManager.insert_or_update({
            'id': 3, 'is_bot': False, 'is_fake': False, 'is_self': False, 'is_scam': False, 'is_verified': False
        })

        TelegramUserDatabaseManager.insert_or_update({
            'id': 4, 'is_bot': False, 'is_fake': False, 'is_self': False, 'is_scam': False, 'is_verified': False
        })

        # Add Media
        media_1 = TelegramMediaDatabaseManager.insert({
            'group_id': 2, 'telegram_id': 159, 'file_name': 'file_001.png', 'extension': 'png',
            'date_time': datetime.datetime.utcnow(), 'mime_type': 'application/pdf', 'size_bytes': 123
        })

        media_2 = TelegramMediaDatabaseManager.insert({
            'group_id': 2, 'telegram_id': 160, 'file_name': 'file_002.png', 'extension': 'png',
            'date_time': datetime.datetime.utcnow(), 'mime_type': 'application/pdf', 'size_bytes': 456
        })

        media_3 = TelegramMediaDatabaseManager.insert({
            'group_id': 2, 'telegram_id': 161, 'file_name': 'file_001.txt', 'extension': 'txt',
            'date_time': datetime.datetime.utcnow(), 'mime_type': 'application/txt', 'size_bytes': 999
        })

        media_4 = TelegramMediaDatabaseManager.insert({
            'group_id': 1, 'telegram_id': 162, 'file_name': 'file_002.txt', 'extension': 'txt',
            'date_time': datetime.datetime.utcnow(), 'mime_type': 'application/txt', 'size_bytes': 99
        })

        # Add Group 1 - Without Any Message
        TelegramGroupDatabaseManager.insert_or_update({
            'id': 1, 'constructor_id': 'A', 'access_hash': 'AAAAAA',
            'fake': False, 'gigagroup': False, 'has_geo': False,
            'participants_count': 1, 'restricted': False,
            'scam': False, 'group_username': 'UN-A',
            'verified': False, 'title': 'UT-01', 'source': '5526986587745'
        })
        TelegramMessageDatabaseManager.insert({
            'id': 90, 'group_id': 1, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 1', 'raw': 'Raw Message 1', 'from_id': 1, 'from_type': None,
            'to_id': None, 'media_id': media_4
        })

        # Add Group 2 - With Previous Messages
        TelegramGroupDatabaseManager.insert_or_update({
            'id': 2, 'constructor_id': 'B', 'access_hash': 'BBBBBB',
            'fake': False, 'gigagroup': False, 'has_geo': False,
            'participants_count': 2, 'restricted': False,
            'scam': False, 'group_username': 'UN-b',
            'verified': False, 'title': 'UT-02', 'source': '5526986587745'
        })
        TelegramMessageDatabaseManager.insert({
            'id': 55, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 1', 'raw': 'Raw Message 1', 'from_id': 3, 'from_type': None,
            'to_id': None, 'media_id': media_1
        })
        TelegramMessageDatabaseManager.insert({
            'id': 56, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 2', 'raw': 'Raw Message 1', 'from_id': 3, 'from_type': None,
            'to_id': None, 'media_id': media_2
        })
        TelegramMessageDatabaseManager.insert({
            'id': 57, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 3', 'raw': 'Raw Message 1', 'from_id': 4, 'from_type': None,
            'to_id': None, 'media_id': media_3
        })
        TelegramMessageDatabaseManager.insert({
            'id': 58, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 3', 'raw': 'Raw Message 4', 'from_id': 3, 'from_type': None,
            'to_id': None, 'media_id': None
        })

    def test_run(self):
        """Test Run Method."""

        target: TelegramStatsGenerator = TelegramStatsGenerator()
        args: Dict = {
            'stats': True,
            'report_folder': '_report',
            'config': 'unittest_configfile.config',
            'limit_days': 30
        }
        data: Dict = {}

        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

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
            # self.assertEqual(4, len(captured.records))
            # self.assertEqual('		Found 2 Groups', captured.records[0].message)
            # self.assertEqual('		ID       	Username	Title', captured.records[1].message)
            # self.assertEqual('		1	UN-A	UT-01', captured.records[2].message)
            # self.assertEqual('		2	UN-b	UT-02', captured.records[3].message)

        # Check Output
        self.assertTrue(os.path.exists(os.path.join('_report', 'stats.txt')))

        # Check Output Content
        report_content = None
        with open(os.path.join('_report', 'stats.txt'), 'r', encoding='UTF-8') as file:
            report_content = file.readlines()

        self.assertEqual('TEx Statistics Report (5526986587745)\n', report_content[0])
        self.assertEqual('Total Groups      : 2\n', report_content[3])
        self.assertEqual('Total Messages    : 5 (~ 0/day)\n', report_content[4])
        self.assertEqual('Total Active Users: 3\n', report_content[5])

        self.assertEqual('**** Messages Statistics for Groups ****\n', report_content[7])
        self.assertEqual('UN-A_1 : 1 messages      : 1 active users\n', report_content[8])
        self.assertEqual('UN-b_2 : 4 messages      : 2 active users\n', report_content[9])

        self.assertEqual('**** Media Statistics for Groups ****\n', report_content[11])
        self.assertEqual('UN-A_1 \n', report_content[12])
        self.assertEqual(
            '\tapplication/txt                                                       : 1 entries       : 99 bytes (0.00 mbytes)\n',
            report_content[13])
        self.assertEqual('UN-b_2 \n', report_content[15])
        self.assertEqual(
            '\tapplication/pdf                                                       : 2 entries       : 579 bytes (0.00 mbytes)\n',
            report_content[16])
        self.assertEqual(
            '\tapplication/txt                                                       : 1 entries       : 999 bytes (0.00 mbytes)\n',
            report_content[17])
