"""Telegram Message Listener Tests."""

import asyncio
import datetime
import logging
import shutil
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock

import pytz
from sqlalchemy import select
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.events import NewMessage
from telethon.tl.types import Channel, ChatBannedRights, ChatPhoto, User, UserStatusRecently

from TEx.core.media_handler import UniversalTelegramMediaHandler
from TEx.database import GROUPS_CACHE, USERS_CACHE
from TEx.database.db_manager import DbManager
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMessageDatabaseManager
from TEx.models.database.telegram_db_model import (
    TelegramMediaOrmEntity, TelegramMessageOrmEntity, TelegramGroupOrmEntity, TelegramUserOrmEntity)
from TEx.modules.telegram_messages_listener import TelegramGroupMessageListener
from TEx.modules.telegram_messages_scrapper import TelegramGroupMessageScrapper
from tests.modules.common import TestsCommon
from tests.modules.mockups_groups_mockup_data import base_groups_mockup_data, base_messages_mockup_data, \
    channel_1_mocked


class TelegramGroupMessageListenerTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('../../config.ini')

        TestsCommon.basic_test_setup()
        GROUPS_CACHE.clear()
        USERS_CACHE.clear()

    def tearDown(self) -> None:
        DbManager.SESSIONS['data'].close()

    def test_run_listen_messages(self):
        """Test Run Method for Listem Telegram Messages."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock(side_effect=self.run_connect_side_effect)

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
        [message for message in base_messages_mockup_data if message.id == 192][0].download_media = mock.AsyncMock(side_effect=self.coroutine_download_mp4)
        [message for message in base_messages_mockup_data if message.id == 4622199][0].download_media = mock.AsyncMock(side_effect=self.coroutine_download_text_plain)
        [message for message in base_messages_mockup_data if message.id == 34357][0].download_media = mock.AsyncMock(side_effect=self.coroutine_download_pdf)

        # Call Test Target Method
        target: TelegramGroupMessageListener = TelegramGroupMessageListener()
        args: Dict = {
            'config': 'unittest_configfile.config',
            'listen': True,
            'ignore_media': False,
            'group_id': '*'
        }
        data: Dict = {
            'telegram_client': telegram_client_mockup
        }

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

            mocked_channels_def = [

                # Channels as Chat
                base_groups_mockup_data.chats[0], base_groups_mockup_data.chats[0], base_groups_mockup_data.chats[0],
                base_groups_mockup_data.chats[0], base_groups_mockup_data.chats[0], base_groups_mockup_data.chats[0],
                base_groups_mockup_data.chats[7], base_groups_mockup_data.chats[7], base_groups_mockup_data.chats[7],
                base_groups_mockup_data.chats[7], base_groups_mockup_data.chats[7], base_groups_mockup_data.chats[7],

                base_groups_mockup_data.chats[12],  # User as Chat
                base_groups_mockup_data.chats[13],  # Chat as Chat
            ]

            # Emulate Dispatcher Calls
            for ix, message in enumerate(base_messages_mockup_data):

                if not message.date:
                    continue

                # Select Mocked Channel for Message
                mocked_channel = mocked_channels_def[ix]

                mocked_event = mock.AsyncMock()
                mocked_event.chat = mocked_channel
                mocked_event.get_chat = mock.AsyncMock(return_value=mocked_channel)
                message.get_chat = mock.AsyncMock(return_value=mocked_channel)

                if message.from_id:
                    mocked_event.from_id = mock.MagicMock()
                    mocked_event.from_id.user_id = message.from_id.user_id

                    mocked_event.get_sender = mock.AsyncMock(return_value=User(
                        id=message.from_id.user_id, is_self=False, contact=False, mutual_contact=False, deleted=False, bot=False,
                        bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False,
                        bot_inline_geo=False, support=False, scam=False, apply_min_photo=True, fake=False,
                        access_hash=8055169766985985814, first_name=f'userfirstname_{message.from_id.user_id}', last_name=None, username=f'userusername_{message.from_id.user_id}',
                        phone=None, photo=None, status=UserStatusRecently(), bot_info_version=None, restriction_reason=[],
                        bot_inline_placeholder=None, lang_code=None))

                mocked_event.message = message

                loop.run_until_complete(
                    target._TelegramGroupMessageListener__handler(event=mocked_event)
                    )

        # Assert Event Handler Added
        telegram_client_mockup.add_event_handler.assert_called_once_with(mock.ANY, NewMessage)

        # Assert Call catch_up
        telegram_client_mockup.catch_up.assert_awaited_once()

        # Asset Call run_until_disconnected
        telegram_client_mockup.run_until_disconnected.assert_awaited_once()

        # Check Logs
        self.assertEqual(18, len(captured.records))
        self.assertEqual('\t\tListening Past Messages...', captured.records[0].message)
        self.assertEqual('\t\tListening New Messages...', captured.records[1].message)
        self.assertEqual('\t\tTelegram Client Disconnected...', captured.records[2].message)
        self.assertEqual('\t\tGroup "10981" not found on DB. Performing automatic synchronization. Consider execute "load_groups" command to perform a full group synchronization (Members and Group Cover Photo).', captured.records[3].message)
        self.assertEqual('\t\tUser "5566" was not found on DB. Performing automatic synchronization.', captured.records[4].message)
        self.assertEqual('\t\tGroup "10984" not found on DB. Performing automatic synchronization. Consider execute "load_groups" command to perform a full group synchronization (Members and Group Cover Photo).', captured.records[5].message)
        self.assertEqual('\t\t\tDownloading Photo from Message 183018 at 2020-05-12 21:22:35', captured.records[6].message)
        self.assertEqual('\t\t\tDownloading Media from Message 183644 (12761.9 Kbytes) as application/vnd.android.package-archive at 2020-05-17 19:20:13', captured.records[7].message)
        self.assertEqual('\t\t\tDownloading Media from Message 183659 (58.8613 Kbytes) as image/webp at 2020-05-17 21:29:30', captured.records[8].message)
        self.assertEqual('\t\t\tDownloading Media from Message 183771 (2258.64 Kbytes) as video/mp4 at 2020-05-18 19:41:47', captured.records[9].message)
        self.assertEqual('\t\tUser "6699" was not found on DB. Performing automatic synchronization.', captured.records[10].message)
        self.assertEqual('\t\t\tDownloading Media from Message 192 (20.1279 Kbytes) as application/x-tgsticker at 2021-08-13 06:51:26', captured.records[11].message)
        self.assertEqual('\t\tUser "1523754667" was not found on DB. Performing automatic synchronization.', captured.records[12].message)
        self.assertEqual('		Group "12099" not found on DB. Performing automatic synchronization. Consider execute "load_groups" command to perform a full group synchronization (Members and Group Cover Photo).', captured.records[13].message)
        self.assertEqual('\t\t\tDownloading Media from Message 4622199 (11.3203 Kbytes) as text/plain at 2022-02-16 15:15:01', captured.records[14].message)
        self.assertEqual('\t\tUser "881571585" was not found on DB. Performing automatic synchronization.', captured.records[15].message)
        self.assertEqual('		Group "12000" not found on DB. Performing automatic synchronization. Consider execute "load_groups" command to perform a full group synchronization (Members and Group Cover Photo).', captured.records[16].message)
        self.assertEqual('\t\t\tDownloading Media from Message 34357 (2900.25 Kbytes) as application/pdf at 2022-02-16 16:05:17', captured.records[17].message)

        # Check Synchronized Groups
        all_groups = DbManager.SESSIONS['data'].execute(
            select(TelegramGroupOrmEntity)
        ).scalars().all()
        self.assertEqual(len(all_groups), 4)

        self.verify_single_group(all_groups[0], '2918368265874677535', '2200278116', False,
                            False, 'CTA', False, 10981, False,
                                False, '5526986587745', 'Channel Title Alpha', False
                                 )

        self.verify_single_group(all_groups[1], '-81612359763615430348', '2200278116', False,
                            False, 'cte', False, 10984, False,
                                False, '5526986587745', 'Channel Title Echo', False
                                 )

        self.verify_single_group(all_groups[2], '', '1103884886', False,
                            False, '', False, 12000, False,
                                False, '5526986587745', 'Chat 12000', False
                                 )

        self.verify_single_group(all_groups[3], '-771864453243322064', '2880827680', False,
                            False, 'johnsnow55', False, 12099, False,
                                False, '5526986587745', 'johnsnow55', False
                                 )

        # Check Synchronized Users
        all_users = DbManager.SESSIONS['data'].execute(
            select(TelegramUserOrmEntity)
        ).scalars().all()
        self.assertEqual(len(all_users), 4)
        self.verify_single_user(all_users[0], user_id=5566, is_bot=False, is_fake=False, is_self=False,
                            is_scam=False, is_verified=False, first_name='userfirstname_5566', last_name=None,
                            username='userusername_5566', phone_number=None, photo_id=None, photo_base64=None,
                            photo_name=None)

        self.verify_single_user(all_users[1], user_id=6699, is_bot=False, is_fake=False, is_self=False,
                                is_scam=False, is_verified=False, first_name='userfirstname_6699', last_name=None,
                                username='userusername_6699', phone_number=None, photo_id=None, photo_base64=None,
                                photo_name=None)

        self.verify_single_user(all_users[2], user_id=881571585, is_bot=False, is_fake=False, is_self=False,
                                is_scam=False, is_verified=False, first_name='userfirstname_881571585', last_name=None,
                                username='userusername_881571585', phone_number=None, photo_id=None, photo_base64=None,
                                photo_name=None)

        self.verify_single_user(all_users[3], user_id=1523754667, is_bot=False, is_fake=False, is_self=False,
                                is_scam=False, is_verified=False, first_name='userfirstname_1523754667', last_name=None,
                                username='userusername_1523754667', phone_number=None, photo_id=None, photo_base64=None,
                                photo_name=None)

        # Check Inserted Messages
        all_messages = DbManager.SESSIONS['data'].execute(
            select(TelegramMessageOrmEntity)
        ).scalars().all()
        self.assertEqual(len(all_messages), 9)

        # Check Message 1
        self.verify_single_message(
            message_obj=all_messages[0], message_id=183017, group_id=10981,
            datetime=datetime.datetime(2020, 5, 12, 21, 19, 22),
            message_content='Message Content', raw_message_content='Message Content',
            to_id=1148933339, from_type='User', from_id=5566, expected_media_id=None
        )

        # Check Message 2 - With a Photo
        self.verify_single_message(
            message_obj=all_messages[1], message_id=183018, group_id=10984,
            datetime=datetime.datetime(2020, 5, 12, 21, 22, 35),
            message_content='Message 2 - With Photo', raw_message_content='Message 2 - With Photo',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=5032983114749683815
        )
        self.verify_media_data(
            expected_media_id=5032983114749683815, filename='183018_photo.jpg',
            extension='.jpg', mime_type='image/jpeg', name=None, height=1280, width=720, size_bytes=146066,
            group_id=10984
        )

        # Check Message 3 - With Binary File
        self.verify_single_message(
            message_obj=all_messages[2], message_id=183644, group_id=10984,
            datetime=datetime.datetime(2020, 5, 17, 19, 20, 13),
            message_content='Message 3 - With Binary File', raw_message_content='Message 3 - With Binary File',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=5042163520989298878
        )
        self.verify_media_data(
            expected_media_id=5042163520989298878, filename='183644_SSH.apk',
            extension='.apk', mime_type='application/vnd.android.package-archive', name=None, height=None,
            width=None, size_bytes=13068140, group_id=10984
        )

        # Check Message 4 - For DoNothing Media Download
        self.verify_single_message(
            message_obj=all_messages[3], message_id=183649, group_id=10984,
            datetime=datetime.datetime(2020, 5, 17, 20, 22, 54),
            message_content='Message 4 - Do Nothing', raw_message_content='Message 4 - Do Nothing',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=None
        )

        # Check Message 5 - With WebImage
        self.verify_single_message(
            message_obj=all_messages[4], message_id=183659, group_id=10984,
            datetime=datetime.datetime(2020, 5, 17, 21, 29, 30),
            message_content='Message 5 - WebImage', raw_message_content='Message 5 - WebImage',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=771772508893348459
        )
        self.verify_media_data(
            expected_media_id=771772508893348459, filename='183659_sticker.webp',
            extension='.webp', mime_type='image/webp', name=None, height=300, width=512, size_bytes=60274,
            group_id=10984
        )

        # Check Message 6 - With MP4
        self.verify_single_message(
            message_obj=all_messages[5], message_id=183771, group_id=10984,
            datetime=datetime.datetime(2020, 5, 18, 19, 41, 47),
            message_content='Message 6 - With MP4', raw_message_content='Message 6 - With MP4',
            to_id=1148953179, from_type='User', from_id=6699,
            expected_media_id=5050896937553756442
        )
        self.verify_media_data(
            expected_media_id=5050896937553756442, filename='183771_unknow.mp4',
            extension='.mp4', mime_type='video/mp4', name=None, height=360, width=640, size_bytes=2312844,
            group_id=10984
        )

        # Check Message 7 - With Sticker
        self.verify_single_message(
            message_obj=all_messages[6], message_id=192, group_id=10984,
            datetime=datetime.datetime(2021, 8, 13, 6, 51, 26),
            message_content='Message 7 - With x-tgsticker', raw_message_content='Message 7 - With x-tgsticker',
            to_id=1331792214, from_type='User', from_id=1523754667,
            expected_media_id=5395606369871073026
        )
        self.verify_media_data(
            expected_media_id=5395606369871073026, filename='192_AnimatedSticker.tgs',
            extension='.mp4', mime_type='application/x-tgsticker', name=None, height=512, width=512,
            size_bytes=20611, group_id=10984
        )

        # Check Message 8 - With text/plain
        self.verify_single_message(
            message_obj=all_messages[7], message_id=4622199, group_id=12099,
            datetime=datetime.datetime(2022, 2, 16, 15, 15, 1),
            message_content='Message 8 - With text/plain', raw_message_content='Message 8 - With text/plain',
            to_id=1287139915, from_type='User', from_id=881571585,
            expected_media_id=4929432170046423539
        )
        self.verify_media_data(
            expected_media_id=4929432170046423539, filename='4622199_1645024499642.txt',
            extension='.txt', mime_type='text/plain', name=None, height=None, width=None, size_bytes=11592,
            group_id=12099
        )

        # Check Message 8 - With text/plain
        self.verify_single_message(
            message_obj=all_messages[8], message_id=34357, group_id=12000,
            datetime=datetime.datetime(2022, 2, 16, 16, 5, 17),
            message_content='Message 9 - With application/pdf',
            raw_message_content='Message 9 - With application/pdf',
            to_id=1496807979, from_type=None, from_id=None,
            expected_media_id=4929533136137618103
        )
        self.verify_media_data(
            expected_media_id=4929533136137618103, filename='34357_mat.pdf',
            extension='.pdf', mime_type='application/pdf', name=None, height=None, width=None, size_bytes=2969855,
            group_id=12000
        )

    def test_run_listen_messages_filtered(self):
        """Test Run Method for Listem Filtered Messages."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock(side_effect=self.run_connect_side_effect)

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
        [message for message in base_messages_mockup_data if message.id == 192][0].download_media = mock.AsyncMock(side_effect=self.coroutine_download_mp4)
        [message for message in base_messages_mockup_data if message.id == 4622199][0].download_media = mock.AsyncMock(side_effect=self.coroutine_download_text_plain)
        [message for message in base_messages_mockup_data if message.id == 34357][0].download_media = mock.AsyncMock(side_effect=self.coroutine_download_pdf)

        # Call Test Target Method
        target: TelegramGroupMessageListener = TelegramGroupMessageListener()
        args: Dict = {
            'config': 'unittest_configfile.config',
            'listen': True,
            'ignore_media': False,
            'group_id': '10984'
        }
        data: Dict = {
            'telegram_client': telegram_client_mockup
        }

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

            # Emulate Dispatcher Calls
            for ix, message in enumerate(base_messages_mockup_data):

                if not message.date:
                    continue

                # Select Mocked Channel for Message
                mocked_channel = base_groups_mockup_data.chats[0] if ix <= 5 else base_groups_mockup_data.chats[7]

                mocked_event = mock.AsyncMock()
                mocked_event.chat = mocked_channel
                mocked_event.get_chat = mock.AsyncMock(return_value=mocked_channel)

                if message.from_id:
                    mocked_event.from_id = mock.MagicMock()
                    mocked_event.from_id.user_id = message.from_id.user_id

                    mocked_event.get_sender = mock.AsyncMock(return_value=User(
                        id=message.from_id.user_id, is_self=False, contact=False, mutual_contact=False, deleted=False, bot=False,
                        bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False,
                        bot_inline_geo=False, support=False, scam=False, apply_min_photo=True, fake=False,
                        access_hash=8055169766985985814, first_name=f'userfirstname_{message.from_id.user_id}', last_name=None, username=f'userusername_{message.from_id.user_id}',
                        phone=None, photo=None, status=UserStatusRecently(), bot_info_version=None, restriction_reason=[],
                        bot_inline_placeholder=None, lang_code=None))

                mocked_event.message = message

                loop.run_until_complete(
                    target._TelegramGroupMessageListener__handler(event=mocked_event)
                    )

        # Assert Event Handler Added
        telegram_client_mockup.add_event_handler.assert_called_once_with(mock.ANY, NewMessage)

        # Assert Call catch_up
        telegram_client_mockup.catch_up.assert_awaited_once()

        # Asset Call run_until_disconnected
        telegram_client_mockup.run_until_disconnected.assert_awaited_once()

        for message in captured.records:
            print(message.message)

        # Check Logs
        self.assertEqual(16, len(captured.records))
        self.assertEqual('\t\tApplied Groups Filtering... 1 selected', captured.records[0].message)
        self.assertEqual('\t\tListening Past Messages...', captured.records[1].message)
        self.assertEqual('\t\tListening New Messages...', captured.records[2].message)
        self.assertEqual('\t\tTelegram Client Disconnected...', captured.records[3].message)
        self.assertEqual('\t\tGroup "10984" not found on DB. Performing automatic synchronization. Consider execute "load_groups" command to perform a full group synchronization (Members and Group Cover Photo).', captured.records[4].message)
        self.assertEqual('\t\t\tDownloading Photo from Message 183018 at 2020-05-12 21:22:35', captured.records[5].message)
        self.assertEqual('\t\t\tDownloading Media from Message 183644 (12761.9 Kbytes) as application/vnd.android.package-archive at 2020-05-17 19:20:13', captured.records[6].message)
        self.assertEqual('\t\t\tDownloading Media from Message 183659 (58.8613 Kbytes) as image/webp at 2020-05-17 21:29:30', captured.records[7].message)
        self.assertEqual('\t\t\tDownloading Media from Message 183771 (2258.64 Kbytes) as video/mp4 at 2020-05-18 19:41:47', captured.records[8].message)
        self.assertEqual('\t\tUser "6699" was not found on DB. Performing automatic synchronization.', captured.records[9].message)
        self.assertEqual('\t\t\tDownloading Media from Message 192 (20.1279 Kbytes) as application/x-tgsticker at 2021-08-13 06:51:26', captured.records[10].message)
        self.assertEqual('\t\tUser "1523754667" was not found on DB. Performing automatic synchronization.', captured.records[11].message)
        self.assertEqual('\t\t\tDownloading Media from Message 4622199 (11.3203 Kbytes) as text/plain at 2022-02-16 15:15:01', captured.records[12].message)
        self.assertEqual('\t\t\t\tMedia Download is not Allowed, Ignoring...', captured.records[13].message)
        self.assertEqual('\t\tUser "881571585" was not found on DB. Performing automatic synchronization.', captured.records[14].message)
        self.assertEqual('\t\t\tDownloading Media from Message 34357 (2900.25 Kbytes) as application/pdf at 2022-02-16 16:05:17', captured.records[15].message)

        # Check Synchronized Groups
        all_groups = DbManager.SESSIONS['data'].execute(
            select(TelegramGroupOrmEntity)
        ).scalars().all()
        self.assertEqual(len(all_groups), 1)

        self.verify_single_group(all_groups[0], '-81612359763615430348', '2200278116', False,
                            False, 'cte', False, 10984, False,
                                False, '5526986587745', 'Channel Title Echo', False
                                 )

        # Check Synchronized Users
        all_users = DbManager.SESSIONS['data'].execute(
            select(TelegramUserOrmEntity)
        ).scalars().all()
        self.assertEqual(len(all_users), 3)
        self.verify_single_user(all_users[0], user_id=6699, is_bot=False, is_fake=False, is_self=False,
                                is_scam=False, is_verified=False, first_name='userfirstname_6699', last_name=None,
                                username='userusername_6699', phone_number=None, photo_id=None, photo_base64=None,
                                photo_name=None)

        self.verify_single_user(all_users[1], user_id=881571585, is_bot=False, is_fake=False, is_self=False,
                                is_scam=False, is_verified=False, first_name='userfirstname_881571585', last_name=None,
                                username='userusername_881571585', phone_number=None, photo_id=None, photo_base64=None,
                                photo_name=None)

        self.verify_single_user(all_users[2], user_id=1523754667, is_bot=False, is_fake=False, is_self=False,
                                is_scam=False, is_verified=False, first_name='userfirstname_1523754667', last_name=None,
                                username='userusername_1523754667', phone_number=None, photo_id=None, photo_base64=None,
                                photo_name=None)

        # Check Inserted Messages
        all_messages = DbManager.SESSIONS['data'].execute(
            select(TelegramMessageOrmEntity)
        ).scalars().all()
        self.assertEqual(len(all_messages), 8)

        # Check Message 1 - With a Photo
        self.verify_single_message(
            message_obj=all_messages[0], message_id=183018, group_id=10984,
            datetime=datetime.datetime(2020, 5, 12, 21, 22, 35),
            message_content='Message 2 - With Photo', raw_message_content='Message 2 - With Photo',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=5032983114749683815
        )
        self.verify_media_data(
            expected_media_id=5032983114749683815, filename='183018_photo.jpg',
            extension='.jpg', mime_type='image/jpeg', name=None, height=1280, width=720, size_bytes=146066,
            group_id=10984
        )

        # Check Message 2 - With Binary File
        self.verify_single_message(
            message_obj=all_messages[1], message_id=183644, group_id=10984,
            datetime=datetime.datetime(2020, 5, 17, 19, 20, 13),
            message_content='Message 3 - With Binary File', raw_message_content='Message 3 - With Binary File',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=5042163520989298878
        )
        self.verify_media_data(
            expected_media_id=5042163520989298878, filename='183644_SSH.apk',
            extension='.apk', mime_type='application/vnd.android.package-archive', name=None, height=None,
            width=None, size_bytes=13068140, group_id=10984
        )

        # Check Message 3 - For DoNothing Media Download
        self.verify_single_message(
            message_obj=all_messages[2], message_id=183649, group_id=10984,
            datetime=datetime.datetime(2020, 5, 17, 20, 22, 54),
            message_content='Message 4 - Do Nothing', raw_message_content='Message 4 - Do Nothing',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=None
        )

        # Check Message 4 - With WebImage
        self.verify_single_message(
            message_obj=all_messages[3], message_id=183659, group_id=10984,
            datetime=datetime.datetime(2020, 5, 17, 21, 29, 30),
            message_content='Message 5 - WebImage', raw_message_content='Message 5 - WebImage',
            to_id=1148953179, from_type=None, from_id=None,
            expected_media_id=771772508893348459
        )
        self.verify_media_data(
            expected_media_id=771772508893348459, filename='183659_sticker.webp',
            extension='.webp', mime_type='image/webp', name=None, height=300, width=512, size_bytes=60274,
            group_id=10984
        )

        # Check Message 5 - With MP4
        self.verify_single_message(
            message_obj=all_messages[4], message_id=183771, group_id=10984,
            datetime=datetime.datetime(2020, 5, 18, 19, 41, 47),
            message_content='Message 6 - With MP4', raw_message_content='Message 6 - With MP4',
            to_id=1148953179, from_type='User', from_id=6699,
            expected_media_id=5050896937553756442
        )
        self.verify_media_data(
            expected_media_id=5050896937553756442, filename='183771_unknow.mp4',
            extension='.mp4', mime_type='video/mp4', name=None, height=360, width=640, size_bytes=2312844,
            group_id=10984
        )

        # Check Message 6 - With Sticker
        self.verify_single_message(
            message_obj=all_messages[5], message_id=192, group_id=10984,
            datetime=datetime.datetime(2021, 8, 13, 6, 51, 26),
            message_content='Message 7 - With x-tgsticker', raw_message_content='Message 7 - With x-tgsticker',
            to_id=1331792214, from_type='User', from_id=1523754667,
            expected_media_id=5395606369871073026
        )
        self.verify_media_data(
            expected_media_id=5395606369871073026, filename='192_AnimatedSticker.tgs',
            extension='.mp4', mime_type='application/x-tgsticker', name=None, height=512, width=512,
            size_bytes=20611, group_id=10984
        )

        # Check Message 7 - With text/plain (But, not Downloaded by Media Filter)
        self.verify_single_message(
            message_obj=all_messages[6], message_id=4622199, group_id=10984,
            datetime=datetime.datetime(2022, 2, 16, 15, 15, 1),
            message_content='Message 8 - With text/plain', raw_message_content='Message 8 - With text/plain',
            to_id=1287139915, from_type='User', from_id=881571585,
            expected_media_id=None
        )

        # Check Message 8 - With text/plain
        self.verify_single_message(
            message_obj=all_messages[7], message_id=34357, group_id=10984,
            datetime=datetime.datetime(2022, 2, 16, 16, 5, 17),
            message_content='Message 9 - With application/pdf',
            raw_message_content='Message 9 - With application/pdf',
            to_id=1496807979, from_type=None, from_id=None,
            expected_media_id=4929533136137618103
        )
        self.verify_media_data(
            expected_media_id=4929533136137618103, filename='34357_mat.pdf',
            extension='.pdf', mime_type='application/pdf', name=None, height=None, width=None, size_bytes=2969855,
            group_id=10984
        )

    def test_run_listen_messages_disabled(self):
        """Test Run Method for Listem Telegram Messages Disabled."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock(side_effect=self.run_connect_side_effect)

        # Setup the IterParticipants Mockup
        async def async_generator_side_effect(items):
            for item in items:
                yield item

        # Mock the the Message Iterator Async Method
        telegram_client_mockup.iter_messages = mock.MagicMock(
            return_value=async_generator_side_effect(base_messages_mockup_data))


        # Call Test Target Method
        target: TelegramGroupMessageListener = TelegramGroupMessageListener()
        args: Dict = {
            'config': 'unittest_configfile.config',
            'listen': False,
            'ignore_media': False,
            'group_id': '*'
        }
        data: Dict = {
            'telegram_client': telegram_client_mockup
        }

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

        # Assert Event Handler Added
        telegram_client_mockup.add_event_handler.assert_not_called()

        # Assert Call catch_up
        telegram_client_mockup.catch_up.mock.ANY, NewMessage()

        # Asset Call run_until_disconnected
        telegram_client_mockup.run_until_disconnected.mock.ANY, NewMessage()

        # Check Logs
        self.assertEqual(1, len(captured.records))
        self.assertEqual('\t\tModule is Not Enabled...', captured.records[0].message)

    def verify_single_group(self, group_obj, access_hash=None, constructor_id=None, fake=None, gigagroup=None, username=None,
                            has_geo=None, group_id=None, restricted=None, scam=None, source=None, title=None,
                            verified=None, group_type=None):

        self.assertEqual(group_obj.access_hash, access_hash)
        self.assertEqual(group_obj.constructor_id, constructor_id)
        self.assertEqual(group_obj.fake, fake)
        self.assertEqual(group_obj.gigagroup, gigagroup)
        self.assertEqual(group_obj.group_username, username)
        self.assertEqual(group_obj.has_geo, has_geo)
        self.assertEqual(group_obj.id, group_id)
        self.assertEqual(group_obj.restricted, restricted)
        self.assertEqual(group_obj.scam, scam)
        self.assertEqual(group_obj.source, source)
        self.assertEqual(group_obj.title, title)
        self.assertEqual(group_obj.verified, verified)

    def verify_single_user(self, user_obj: TelegramUserOrmEntity, user_id=None, is_bot=None, is_fake=None, is_self=None,
                           is_scam=None, is_verified=None, first_name=None, last_name=None, username=None,
                           phone_number=None, photo_id=None, photo_base64=None, photo_name=None) -> None:

        self.assertEqual(user_obj.id, user_id)
        self.assertEqual(user_obj.is_bot, is_bot)
        self.assertEqual(user_obj.is_fake, is_fake)
        self.assertEqual(user_obj.is_self, is_self)
        self.assertEqual(user_obj.is_scam, is_scam)
        self.assertEqual(user_obj.is_verified, is_verified)
        self.assertEqual(user_obj.first_name, first_name)
        self.assertEqual(user_obj.last_name, last_name)
        self.assertEqual(user_obj.username, username)
        self.assertEqual(user_obj.phone_number, phone_number)
        self.assertEqual(user_obj.photo_id, photo_id)
        self.assertEqual(user_obj.photo_base64, photo_base64)
        self.assertEqual(user_obj.photo_name, photo_name)

    def verify_single_message(self, message_obj, message_id, group_id, datetime, message_content,
                              raw_message_content, to_id, from_id, from_type, expected_media_id) -> None:
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
                DbManager.SESSIONS['data'].execute(
                    select(TelegramMediaOrmEntity)
                    .where(TelegramMediaOrmEntity.telegram_id == expected_media_id)
                    .where(TelegramMediaOrmEntity.group_id == group_id)
                    .limit(1)
                ).one()[0].id,
                message_obj.media_id
            )

    def verify_media_data(self, expected_media_id, filename, extension, mime_type, name, height, width, size_bytes,
                          group_id) -> None:

        db_result = DbManager.SESSIONS['data'].execute(
            select(TelegramMediaOrmEntity)
            .where(TelegramMediaOrmEntity.telegram_id == expected_media_id)
            .where(TelegramMediaOrmEntity.group_id == group_id)
            .limit(1)).one(),

        media_obj = db_result[0][0]

        self.assertIsNotNone(media_obj)
        self.assertEqual(media_obj.file_name, filename)
        self.assertEqual(media_obj.extension, extension)
        self.assertEqual(media_obj.mime_type, mime_type)
        self.assertEqual(media_obj.name, name)
        self.assertEqual(media_obj.height, height)
        self.assertEqual(media_obj.width, width)
        self.assertEqual(media_obj.size_bytes, size_bytes)

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

    async def coroutine_download_text_plain(self, path) -> str:

        # Copy Resources
        shutil.copyfile('resources/1645024499642.txt', '_data/resources/1645024499642.txt')

        # Return the Path
        return '_data/resources/1645024499642.txt'

    async def coroutine_download_sticker(self, path) -> str:

        # Copy Resources
        shutil.copyfile('resources/AnimatedSticker.tgs', '_data/resources/AnimatedSticker.tgs')

        # Return the Path
        return '_data/resources/AnimatedSticker.tgs'

    async def coroutine_download_pdf(self, path) -> str:

        # Copy Resources
        shutil.copyfile('resources/mat.pdf', '_data/resources/mat.pdf')

        # Return the Path
        return '_data/resources/mat.pdf'

