"""Telegram Report - Export Texts Generator."""

import asyncio
import datetime
import logging
import os.path
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
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMediaDatabaseManager, \
    TelegramMessageDatabaseManager
from TEx.models.database.telegram_db_model import (
    TelegramGroupOrmEntity,
    TelegramMediaOrmEntity, TelegramMessageOrmEntity, TelegramUserOrmEntity,
)
from TEx.modules.execution_configuration_handler import ExecutionConfigurationHandler
from TEx.modules.telegram_messages_scrapper import TelegramGroupMessageScrapper
from TEx.modules.telegram_report_generator.telegram_export_text_generator import TelegramExportTextGenerator
from TEx.modules.telegram_report_generator.telegram_html_report_generator import TelegramReportGenerator
from tests.modules.common import TestsCommon
from tests.modules.mockups_groups_mockup_data import base_groups_mockup_data, base_messages_mockup_data, \
    base_users_mockup_data


class TelegramExportTextGeneratorTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('../../config.ini')

        DirectoryManagerUtils.ensure_dir_struct('_data')
        DirectoryManagerUtils.ensure_dir_struct('_data/resources')
        DirectoryManagerUtils.ensure_dir_struct('_data/media')
        DirectoryManagerUtils.ensure_dir_struct('_data/media/2')

        DbInitializer.init(data_path='_data/')

        # Reset SQLlite Groups
        DbManager.SESSIONS['data'].execute(delete(TelegramMessageOrmEntity))
        DbManager.SESSIONS['data'].execute(delete(TelegramGroupOrmEntity))
        DbManager.SESSIONS['data'].execute(delete(TelegramMediaOrmEntity))
        DbManager.SESSIONS['data'].commit()

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
            'message': 'Message 1', 'raw': 'Raw Message 1', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': None
        })
        TelegramMessageDatabaseManager.insert({
            'id': 56, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 2', 'raw': 'Raw Message 2', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': None
        })
        TelegramMessageDatabaseManager.insert({
            'id': 57, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 2', 'raw': 'Raw Message 3', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': None
        })
        TelegramMessageDatabaseManager.insert({
            'id': 58, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 3', 'raw': 'Raw Message 4 - http://www.url.domain.com', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': None
        })

        # Add Group 3 - With Previous Messages
        TelegramGroupDatabaseManager.insert_or_update({
            'id': 3, 'constructor_id': 'B', 'access_hash': 'BBBBBB',
            'fake': False, 'gigagroup': False, 'has_geo': False,
            'participants_count': 2, 'restricted': False,
            'scam': False, 'group_username': 'UN-c',
            'verified': False, 'title': 'UT-03', 'source': '5526986587745'
        })
        TelegramMessageDatabaseManager.insert({
            'id': 60, 'group_id': 3, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 7', 'raw': 'Raw Message 1', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': None
        })
        TelegramMessageDatabaseManager.insert({
            'id': 61, 'group_id': 3, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 8', 'raw': 'Raw Message 2', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': None
        })
        TelegramMessageDatabaseManager.insert({
            'id': 62, 'group_id': 3, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 9', 'raw': 'Raw Message 3', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': None
        })
        TelegramMessageDatabaseManager.insert({
            'id': 63, 'group_id': 3, 'date_time': datetime.datetime.now(tz=pytz.utc),
            'message': 'Message 10', 'raw': 'Raw Message 4 - http://www.url.domain.com/2', 'from_id': None,
            'from_type': None, 'to_id': None, 'media_id': None
        })

        DbManager.SESSIONS['data'].commit()

    def tearDown(self) -> None:
        DbManager.SESSIONS['data'].close()

    def test_run_generate_report_all(self):
        """Test Run Method."""

        # Call Test Target Method
        target: TelegramExportTextGenerator = TelegramExportTextGenerator()
        args: Dict = {
            'export_text': True,
            'config': 'unittest_configfile.config',
            'report_folder': '_report',
            'group_id': '*',
            'order_desc': True,
            'filter': 'Message',
            'limit_days': 30,
            'regex': '(http[s]?:\/\/[^\"\',]*)'
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

        # Check Output Files
        self.assertTrue(
            os.path.exists(os.path.join('_report', f'result_UN-b_2.txt'))
        )
        self.assertTrue(
            os.path.exists(os.path.join('_report', f'result_UN-c_3.txt'))
        )

        # Check Output Files Content
        with open(os.path.join('_report', f'result_UN-b_2.txt')) as file:
            content = file.readlines()
            self.assertEqual(1, len(content))
            self.assertEqual('http://www.url.domain.com\n', content[0])

        with open(os.path.join('_report', f'result_UN-c_3.txt')) as file:
            content = file.readlines()
            self.assertEqual(1, len(content))
            self.assertEqual('http://www.url.domain.com/2\n', content[0])

    def test_run_generate_report_filtered(self):
        """Test Run Method."""

        # Call Test Target Method
        target: TelegramExportTextGenerator = TelegramExportTextGenerator()
        args: Dict = {
            'export_text': True,
            'config': 'unittest_configfile.config',
            'report_folder': '_report',
            'group_id': '2',
            'order_desc': True,
            'filter': 'Message',
            'limit_days': 30,
            'regex': '((.*https:\/\/.*)|(.*http:\/\/.*))'
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

        # Check Output Files
        self.assertTrue(
            os.path.exists(os.path.join('_report', f'result_UN-b_2.txt'))
        )
        self.assertFalse(
            os.path.exists(os.path.join('_report', f'result_UN-c_3.txt'))
        )

    def test_run_disabled(self):
        """Test Run Method Disabled."""

        # Call Test Target Method
        target: TelegramExportTextGenerator = TelegramExportTextGenerator()
        args: Dict = {
            'export_text': False,
            'config': 'unittest_configfile.config',
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        with self.assertLogs(level=logging.DEBUG) as captured:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                target.run(
                    config=self.config,
                    args=args,
                    data=data
                )
            )

            # Check Output Logs
            expected_log_messages = [
                '\t\tModule is Not Enabled...',
            ]

            self.assertEqual(len(expected_log_messages), len(captured.records))
            for ix, record in enumerate(captured.records):
                self.assertEqual(expected_log_messages[ix], record.message)

    def test_run_invalid_regex(self):
        """Test Run Method with Invalid RegEx."""

        # Call Test Target Method
        target: TelegramExportTextGenerator = TelegramExportTextGenerator()
        args: Dict = {
            'export_text': True,
            'config': 'unittest_configfile.config',
            'report_folder': '_report',
            'group_id': '*',
            'order_desc': True,
            'filter': 'Message',
            'limit_days': 30,
            'regex': '^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$'
        }
        data: Dict = {'internals': {'panic': False}}
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

            # Check Output Logs
            expected_log_messages = [
                '\t\tFound 2 Groups',
                '\t\tProcessing "UT-02" (2)',
                '\t\t\tRetrieving Messages',
                '\t\t\tFiltering',
                '\t\tInvalid RegEx: "bad character range \\w-\\." - Pattern: ^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$'
            ]

            self.assertEqual(len(expected_log_messages), len(captured.records))
            for ix, record in enumerate(captured.records):
                self.assertEqual(expected_log_messages[ix], record.message)

        self.assertTrue(data['internals']['panic'])
