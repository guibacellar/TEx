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
        [message for message in base_messages_mockup_data if message.id == 183659][0].download_media = mock.AsyncMock(side_effect=self.coroutine_download_websticker)
        [message for message in base_messages_mockup_data if message.id == 183771][0].download_media = mock.AsyncMock(side_effect=self.coroutine_download_mp4)

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
            self.assertEqual(8, len(captured.records))
            self.assertEqual('		Found 2 Groups', captured.records[0].message)
            self.assertEqual('		Download Messages from "UT-01" > Last Offset: None', captured.records[1].message)
            self.assertEqual('			Downloading Photo from Message 183018', captured.records[2].message)
            self.assertEqual('			Downloading Media from Message 183644 (12761.9 Kbytes) as application/vnd.android.package-archive', captured.records[3].message)
            self.assertEqual('			Downloading Media from Message 183659 (58.8613 Kbytes) as image/webp', captured.records[4].message)
            self.assertEqual('			Downloading Media from Message 183771 (2258.64 Kbytes) as video/mp4', captured.records[5].message)
            self.assertEqual('		Download Messages from "UT-01" > Last Offset: 183771', captured.records[6].message)
            self.assertEqual('		Download Messages from "UT-02" > Last Offset: 55', captured.records[7].message)

        # Check all Messages in SQLlite DB
        all_messages = DbManager.SESSIONS['data'].execute(
            select(TelegramMessageOrmEntity).where(TelegramMessageOrmEntity.group_id == 1)
        ).scalars().all()

        self.assertEqual(6, len(all_messages))

        # Check Message 1
        self.verify_single_message(
            message_obj=all_messages[0], message_id=183017, group_id=1, datetime=datetime.datetime(2020, 5, 12, 21, 19, 22),
            message_content='Message Content', raw_message_content='Message Content',
            to_id=1148953179, from_type='User', from_id=5566, expected_media_id=None
        )

        # Check Message 2 - With a Photo
        self.verify_single_message(
            message_obj=all_messages[1], message_id=183018, group_id=1, datetime=datetime.datetime(2020, 5, 12, 21, 22, 35),
            message_content='Message 2 - With Photo', raw_message_content='Message 2 - With Photo',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=5032983114749683815
        )

        # Check Message 3 - With Binary File
        self.verify_single_message(
            message_obj=all_messages[2], message_id=183644, group_id=1, datetime=datetime.datetime(2020, 5, 17, 19, 20, 13),
            message_content='Message 3 - With Binary File', raw_message_content='Message 3 - With Binary File',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=5042163520989298878
        )

        # Check Message 4 - For DoNothing Media Download
        self.verify_single_message(
            message_obj=all_messages[3], message_id=183649, group_id=1, datetime=datetime.datetime(2020, 5, 17, 20, 22, 54),
            message_content='Message 4 - Do Nothing', raw_message_content='Message 4 - Do Nothing',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=None
        )

        # Check Message 5 - With WebImage
        self.verify_single_message(
            message_obj=all_messages[4], message_id=183659, group_id=1, datetime=datetime.datetime(2020, 5, 17, 21, 29, 30),
            message_content='Message 5 - WebImage', raw_message_content='Message 5 - WebImage',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=771772508893348459
        )

        # Check Message 6 - With MP4
        self.verify_single_message(
            message_obj=all_messages[5], message_id=183771, group_id=1, datetime=datetime.datetime(2020, 5, 18, 19, 41, 47),
            message_content='Message 6 - With MP4', raw_message_content='Message 6 - With MP4',
            to_id=1148953179, from_type='User', from_id=6699,
            expected_media_id=5050896937553756442
        )

    def verify_single_message(self, message_obj, message_id, group_id, datetime, message_content, raw_message_content, to_id, from_id, from_type, expected_media_id) -> None:
        self.assertEqual(message_id, message_obj.id)
        self.assertEqual(group_id, message_obj.group_id)
        self.assertEqual(datetime, message_obj.date_time)
        self.assertEqual(message_content, message_obj.message)
        self.assertEqual(raw_message_content, message_obj.raw)
        self.assertEqual(from_id, message_obj.from_id)
        self.assertEqual(from_type, message_obj.from_type)
        self.assertEqual(to_id, message_obj.to_id)

        if expected_media_id:
            self.assertEqual(
                DbManager.SESSIONS['media_1'].execute(
                    select(TelegramMediaOrmEntity).where(TelegramMediaOrmEntity.telegram_id == expected_media_id).limit(1)).one()[0].id,
                    message_obj.media_id
                )


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

    async def coroutine_download_websticker(self, path) -> str:

        # Copy Resources
        shutil.copyfile('resources/sticker.webp', '_data/resources/sticker.webp')

        # Return the Path
        return '_data/resources/sticker.webp'

    async def coroutine_download_mp4(self, path) -> str:

        # Copy Resources
        shutil.copyfile('resources/unknow.mp4', '_data/resources/unknow.mp4')

        # Return the Path
        return '_data/resources/unknow.mp4'

