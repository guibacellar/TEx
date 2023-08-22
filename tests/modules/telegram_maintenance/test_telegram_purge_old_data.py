"""Telegram Purge Old Data Tests."""

import asyncio
import datetime
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
from TEx.modules.telegram_maintenance.telegram_purge_old_data import TelegramMaintenancePurgeOldData
from TEx.modules.telegram_messages_scrapper import TelegramGroupMessageScrapper
from TEx.modules.telegram_report_generator.telegram_html_report_generator import TelegramReportGenerator
from tests.modules.common import TestsCommon
from tests.modules.mockups_groups_mockup_data import base_groups_mockup_data, base_messages_mockup_data, \
    base_users_mockup_data


class TelegramMaintenancePurgeOldDataTest(unittest.TestCase):

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

        # Add Media
        shutil.copy(
            os.path.join('resources', 'mat.pdf'),
            os.path.join('_data', 'media', '2', '55_mat.pdf')
            )
        media_id = TelegramMediaDatabaseManager.insert(
            {
                'file_name': '55_mat.pdf',
                'telegram_id': 999,
                'group_id': 2,
                'extension': 'pdf',
                'height': 0,
                'width': 0,
                'date_time': datetime.datetime.utcnow()-datetime.timedelta(days=31),
                'mime_type': 'application/pdf',
                'size_bytes': 58964,
                'title': 'mat pdf',
                'name': 'mat'
            }
        )

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
        TelegramMessageDatabaseManager.insert({
            'id': 55, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc)-datetime.timedelta(days=31),
            'message': 'Message 1', 'raw': 'Raw Message 1', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': media_id
        })
        TelegramMessageDatabaseManager.insert({
            'id': 56, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc)-datetime.timedelta(days=30),
            'message': 'Message 2', 'raw': 'Raw Message 2', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': None
        })
        TelegramMessageDatabaseManager.insert({
            'id': 57, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc)-datetime.timedelta(days=29),
            'message': 'Message 2', 'raw': 'Raw Message 2', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': None
        })
        TelegramMessageDatabaseManager.insert({
            'id': 58, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc)-datetime.timedelta(days=28),
            'message': 'Message 3', 'raw': 'Raw Message 3', 'from_id': None, 'from_type': None,
            'to_id': None, 'media_id': None
        })

        DbManager.SESSIONS['data'].commit()

    def tearDown(self) -> None:
        DbManager.SESSIONS['data'].close()

    def test_purge_old_data_disabled(self):
        """Test Run Method for Scrap Telegram Groups."""

        # Call Test Target Method
        target: TelegramMaintenancePurgeOldData = TelegramMaintenancePurgeOldData()
        args: Dict = {
            'config': 'unittest_configfile.config',
            'purge_old_data': False,
            'limit_days': 30
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Execute Module
        with self.assertLogs() as captured:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                target.run(
                    config=self.config,
                    args=args,
                    data=data
                )
            )

            self.assertEqual("\t\tModule is Not Enabled...", captured.records[0].message)

    def test_purge_old_data(self):
        """Test Run Method for Scrap Telegram Groups."""

        # Call Test Target Method
        target: TelegramMaintenancePurgeOldData = TelegramMaintenancePurgeOldData()
        args: Dict = {
            'config': 'unittest_configfile.config',
            'purge_old_data': True,
            'limit_days': 30
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Validate Data Before Execution
        self.assertEqual(2, len(TelegramGroupDatabaseManager.get_all_by_phone_number(phone_number='5526986587745')))
        self.assertEqual(0, len(TelegramMessageDatabaseManager.get_all_messages_from_group(group_id=1)))
        self.assertEqual(4, len(TelegramMessageDatabaseManager.get_all_messages_from_group(group_id=2)))
        self.assertEqual(1, len(TelegramMediaDatabaseManager.get_all_medias_from_group_and_mimetype(group_id=2, mime_type='application/pdf').all()))
        self.assertTrue(os.path.exists(os.path.join('_data', 'media', '2', '55_mat.pdf')))

        # Execute Module
        with self.assertLogs() as captured:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                target.run(
                    config=self.config,
                    args=args,
                    data=data
                )
            )

        # Check DB Groups
        self.assertEqual(2, len(TelegramGroupDatabaseManager.get_all_by_phone_number(phone_number='5526986587745')))

        # Check DB Messages
        self.assertEqual(0, len(TelegramMessageDatabaseManager.get_all_messages_from_group(group_id=1)))
        self.assertEqual(2, len(TelegramMessageDatabaseManager.get_all_messages_from_group(group_id=2)))

        # Check DB Medias
        self.assertEqual(0, len(TelegramMediaDatabaseManager.get_all_medias_from_group_and_mimetype(group_id=2, mime_type='application/pdf').all()))

        # Check File is Deleted
        self.assertFalse(os.path.exists(os.path.join('_data', 'media', '2', '55_mat.pdf')))
