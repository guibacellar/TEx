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

        # TODO: Refactory: Add this to a new method

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

    def test_run_download_messages(self):
        """Test Run Method for Scrap Telegram Groups."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock(side_effect=self.run_connect_side_effect)

        # Setup the Download Profile Photos Mockup
        #telegram_client_mockup.download_profile_photo = mock.AsyncMock(side_effect=self.coroutine_downloadfile)

        # Setup the IterParticipants Mockup
        async def async_generator_side_effect(items):
            for item in items:
                yield item

        # Mock the the Message Iterator Async Method
        telegram_client_mockup.iter_messages = mock.MagicMock(return_value=async_generator_side_effect(base_messages_mockup_data))

        # Add the Async Mocks to Messages
        [message for message in base_messages_mockup_data if message.id == 183018][0].download_media = mock.AsyncMock(side_effect=self.coroutine_download_photo)
        [message for message in base_messages_mockup_data if message.id == 183644][0].download_media = mock.AsyncMock(side_effect=self.coroutine_download_binary)

        # Call Test Target Method
        target: TelegramGroupMessageScrapper = TelegramGroupMessageScrapper()
        args: Dict = {
            'target_phone_number': 'UT-PHONE',  # TODO: Make a new Test when the target_phone_number has no Groups
            'data_path': '_data',
            'download_messages': True,
            'ignore_media': False
        }
        data: Dict = {
            'telegram_client': telegram_client_mockup
        }

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
            self.assertEqual(6, len(captured.records))
            self.assertEqual('		Found 2 Groups', captured.records[0].message)
            self.assertEqual('		Download Messages from "UT-01" > Last Offset: None', captured.records[1].message)
            self.assertEqual('			Downloading Photo from Message 183018', captured.records[2].message)
            self.assertEqual('			Downloading Media from Message 183644 (12761.9 Kbytes) as application/vnd.android.package-archive', captured.records[3].message)
            self.assertEqual('		Download Messages from "UT-01" > Last Offset: 183649', captured.records[4].message)
            self.assertEqual('		Download Messages from "UT-02" > Last Offset: 55', captured.records[5].message)

        # Check all Messages in SQLlite DB
        all_messages = DbManager.SESSIONS['data'].execute(
            select(TelegramMessageOrmEntity).where(TelegramMessageOrmEntity.group_id == 1)
        ).scalars().all()

        self.assertEqual(4, len(all_messages))

        # Check Message 1
        self.assertEqual(183017, all_messages[0].id)
        self.assertEqual(1, all_messages[0].group_id)
        self.assertIsNone(all_messages[0].media_id)
        self.assertEqual(datetime.datetime(2020, 5, 12, 21, 19, 22), all_messages[0].date_time)
        self.assertEqual('Message Content', all_messages[0].message)
        self.assertEqual('Message Content', all_messages[0].raw)
        self.assertEqual(5566, all_messages[0].from_id)
        self.assertEqual('User', all_messages[0].from_type)
        self.assertEqual(1148953179, all_messages[0].to_id)

        # Check Message 2
        self.assertEqual(183018, all_messages[1].id)
        self.assertEqual(1, all_messages[1].group_id)
        self.assertEqual(datetime.datetime(2020, 5, 12, 21, 22, 35), all_messages[1].date_time)
        self.assertEqual('Message 2', all_messages[1].message)
        self.assertEqual('Message 2', all_messages[1].raw)
        self.assertIsNone(all_messages[1].from_id)
        self.assertIsNone(all_messages[1].from_type)
        self.assertEqual(1148953179, all_messages[1].to_id)
        self.assertEqual(
            DbManager.SESSIONS['media_1'].execute(select(TelegramMediaOrmEntity).where(TelegramMediaOrmEntity.telegram_id==5032983114749683815).limit(1)).one()[0].id,
            all_messages[1].media_id
        )

        # Check Message 3
        self.assertEqual(183644, all_messages[2].id)
        self.assertEqual(1, all_messages[2].group_id)
        self.assertEqual(datetime.datetime(2020, 5, 17, 19, 20, 13), all_messages[2].date_time)
        self.assertEqual('Message 3', all_messages[2].message)
        self.assertEqual('Message 3', all_messages[2].raw)
        self.assertIsNone(all_messages[2].from_id)
        self.assertIsNone(all_messages[2].from_type)
        self.assertEqual(1148953179, all_messages[2].to_id)
        self.assertEqual(
            DbManager.SESSIONS['media_1'].execute(select(TelegramMediaOrmEntity).where(TelegramMediaOrmEntity.telegram_id==5042163520989298878).limit(1)).one()[0].id,
            all_messages[2].media_id
        )

        # Check Message 4
        self.assertEqual(183649, all_messages[3].id)
        self.assertEqual(1, all_messages[3].group_id)
        self.assertEqual(datetime.datetime(2020, 5, 17, 20, 22, 54), all_messages[3].date_time)
        self.assertEqual('Message 4', all_messages[3].message)
        self.assertEqual('Message 4', all_messages[3].raw)
        self.assertIsNone(all_messages[3].from_id)
        self.assertIsNone(all_messages[3].from_type)
        self.assertEqual(1148953179, all_messages[3].to_id)

    def run_connect_side_effect(self, param):

        if isinstance(param, GetDialogsRequest):
            return base_groups_mockup_data

        raise Exception(type(param))

    async def coroutine_download_photo(self, path) -> str:

        # Copy Resources
        shutil.copyfile('resources/122761750_387013276008970_8208112669996447119_n.jpg',
                        '_data/resources/test_run_connect.jpg')

        # Return the Path
        return '_data/resources/test_run_connect.jpg'

    async def coroutine_download_binary(self, path) -> str:

        # Copy Resources
        shutil.copyfile('resources/demo.apk', '_data/resources/demo.apk')

        # Return the Path
        return '_data/resources/demo.apk'
