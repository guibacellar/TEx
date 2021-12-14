"""Telegram Groups Scrapper Tests."""

import shutil
import asyncio
import unittest
from unittest import mock
from typing import Dict
from configparser import ConfigParser

from telethon.tl.functions.messages import GetDialogsRequest

from TEx.core.dir_manager import DirectoryManagerUtils
from TEx.database.db_initializer import DbInitializer
from TEx.modules.telegram_groups_scrapper import TelegramGroupScrapper
from tests.modules.mockups_groups_mockup_data import base_groups_mockup_data, b64_group_pic_image, \
    base_users_mockup_data


class TelegramConnectorTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('../../config.ini')

        DirectoryManagerUtils.ensure_dir_struct('_data')
        DirectoryManagerUtils.ensure_dir_struct('_data/resources')

        DbInitializer.init(data_path='_data/', args={})

    def test_run_download_groups(self):
        """Test Run Method for Scrap Telegram Groups."""


        # Setup Mock
        telegram_client_mockup = mock.AsyncMock(side_effect=self.run_connect_side_effect)

        # Setup the Download Profile Photos Mockup
        telegram_client_mockup.download_profile_photo = mock.AsyncMock(side_effect=self.coroutine_downloadfile)

        # Setup the IterParticipants Mockup
        async def async_generator_side_effect(items):
            for item in items:
                yield item
        telegram_client_mockup.iter_participants = mock.MagicMock(return_value=async_generator_side_effect(base_users_mockup_data))

        target: TelegramGroupScrapper = TelegramGroupScrapper()
        args: Dict = {
            'load_groups': True,
            'target_phone_number': 'MyTestPhoneNumber3',
            'refresh_profile_photos': True,
            'data_path': '_data'
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

            # # Check Logs
            # self.assertEqual(2, len(captured.records))
            # self.assertEqual('		User Authorized on Telegram: True', captured.records[1].message)

        # Validate Mock Calls
        # telegram_client_mockup.start.assert_awaited_once_with(phone='MyTestPhoneNumber')

        # # Validate Data Result Dict
        # self.assertEqual('MyTestApiID', data['telegram_connection']['api_id'])
        # self.assertEqual('MyTestApiHash', data['telegram_connection']['api_hash'])
        # self.assertEqual('MyTestPhoneNumber', data['telegram_connection']['target_phone_number'])
        # self.assertEqual(started_telegram_client_mockup, data['telegram_client'])

    def run_connect_side_effect(self, param):

        if isinstance(param, GetDialogsRequest):
            return base_groups_mockup_data

        raise Exception(type(param))

    async def coroutine_downloadfile(self, entity, file, download_big) -> str:

        # Copy Resources
        shutil.copyfile('resources/122761750_387013276008970_8208112669996447119_n.jpg', '_data/resources/test_run_connect.jpg')

        # Return the Path
        return '_data/resources/test_run_connect.jpg'
