"""Telegram Groups List Tests."""

import asyncio
import logging
import unittest
from configparser import ConfigParser
from typing import Dict

from TEx.database.telegram_group_database import TelegramGroupDatabaseManager
from TEx.modules.telegram_groups_list import TelegramGroupList
from TEx.modules.telegram_groups_scrapper import TelegramGroupScrapper
from tests.modules.common import TestsCommon


class TelegramGroupListTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('../../config.ini')

        TestsCommon.basic_test_setup()

        # Add Group 1 - Without Any Message
        TelegramGroupDatabaseManager.insert_or_update({
            'id': 1, 'constructor_id': 'A', 'access_hash': 'AAAAAA',
            'fake': False, 'gigagroup': False, 'has_geo': False,
            'participants_count': 1, 'restricted': False,
            'scam': False, 'group_username': 'UN-A',
            'verified': False, 'title': 'UT-01', 'source': '5526986587745'
        })

        # Add Group 2 - With Previous Messages
        TelegramGroupDatabaseManager.insert_or_update({
            'id': 2, 'constructor_id': 'B', 'access_hash': 'BBBBBB',
            'fake': False, 'gigagroup': False, 'has_geo': False,
            'participants_count': 2, 'restricted': False,
            'scam': False, 'group_username': 'UN-b',
            'verified': False, 'title': 'UT-02', 'source': '5526986587745'
        })

    def test_run(self):
        """Test Run Method."""

        target: TelegramGroupScrapper = TelegramGroupList()
        args: Dict = {
            'list_groups': True,
            'config': 'unittest_configfile.config',
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

            # Check Logs
            self.assertEqual(4, len(captured.records))
            self.assertEqual('		Found 2 Groups', captured.records[0].message)
            self.assertEqual('		ID       	Username	Title', captured.records[1].message)
            self.assertEqual('		1	UN-A	UT-01', captured.records[2].message)
            self.assertEqual('		2	UN-b	UT-02', captured.records[3].message)

    def test_run_disabled(self):
        """Test Run Method Disabled."""

        target: TelegramGroupScrapper = TelegramGroupList()
        args: Dict = {
            'list_groups': False,
            'config': 'unittest_configfile.config',
        }
        data: Dict = {}

        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        with self.assertLogs('TelegramExplorer', level=logging.DEBUG) as captured:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                target.run(
                    config=self.config,
                    args=args,
                    data=data
                )
            )

            # Check Logs
            self.assertEqual(1, len(captured.records))
            self.assertEqual('		Module is Not Enabled...', captured.records[0].message)
