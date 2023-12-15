"""Telegram Groups Scrapper Tests."""

import asyncio
import logging
import shutil
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock

from sqlalchemy import select
from telethon.errors.rpcerrorlist import ChannelPrivateError
from telethon.tl.functions.messages import GetDialogsRequest

from TEx.database.db_manager import DbManager
from TEx.models.database.telegram_db_model import (
    TelegramGroupOrmEntity,
    TelegramUserOrmEntity,
)
from TEx.modules.telegram_groups_scrapper import TelegramGroupScrapper
from tests.modules.common import TestsCommon
from tests.modules.mockups_groups_mockup_data import base_groups_mockup_data, base_users_mockup_data


class TelegramGroupScrapperTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('../../config.ini')

        TestsCommon.basic_test_setup()

    def tearDown(self) -> None:
        DbManager.SESSIONS['data'].close()

    def test_run_download_groups_simulate_channel_private_error(self):
        """Test Run Method for Scrap Telegram Groups - Simulates a ChannelPrivateError."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock(side_effect=self.run_connect_side_effect)

        # Setup the Download Profile Photos Mockup
        telegram_client_mockup.download_profile_photo = mock.AsyncMock(side_effect=self.coroutine_downloadfile)

        telegram_client_mockup.iter_participants = mock.MagicMock(side_effect=ChannelPrivateError(''))

        target: TelegramGroupScrapper = TelegramGroupScrapper()
        args: Dict = {
            'load_groups': True,
            'config': 'unittest_configfile.config',
            'refresh_profile_photos': True,
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

            # Check Logs
            self.assertEqual(15, len(captured.records))
            self.assertEqual('		Enumerating Groups', captured.records[0].message)
            self.assertEqual('		Processing "Channel Title Alpha (10981)" Members and Group Profile Picture', captured.records[1].message)
            self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...', captured.records[2].message)

            self.assertEqual('		Processing "Channel Title Beta (10982)" Members and Group Profile Picture', captured.records[3].message)
            self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...', captured.records[4].message)

            self.assertEqual('		Processing "Channel Title Delta (10983)" Members and Group Profile Picture', captured.records[5].message)
            self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...', captured.records[6].message)

            self.assertEqual('		Processing "Channel Title Echo (10984)" Members and Group Profile Picture', captured.records[7].message)
            self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...', captured.records[8].message)

            self.assertEqual('		Processing "Channel Title Charlie (10985)" Members and Group Profile Picture', captured.records[9].message)
            self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...', captured.records[10].message)

            self.assertEqual('		Processing "Channel Title Fox (10989)" Members and Group Profile Picture', captured.records[11].message)
            self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...', captured.records[12].message)

    def test_run_download_groups_simulate_peer_channel_restrictions_error(self):
        """Test Run Method for Scrap Telegram Groups - Simulates a PeerChannel Restrictions."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock(side_effect=self.run_connect_side_effect)

        # Setup the Download Profile Photos Mockup
        telegram_client_mockup.download_profile_photo = mock.AsyncMock(side_effect=self.coroutine_downloadfile)

        telegram_client_mockup.iter_participants = mock.MagicMock(side_effect=ValueError('PeerChannel Restrictions'))

        target: TelegramGroupScrapper = TelegramGroupScrapper()
        args: Dict = {
            'load_groups': True,
            'config': 'unittest_configfile.config',
            'refresh_profile_photos': True,
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

            # Check Logs
            self.assertEqual(15, len(captured.records))
            self.assertEqual('		Enumerating Groups', captured.records[0].message)
            self.assertEqual('		Processing "Channel Title Alpha (10981)" Members and Group Profile Picture', captured.records[1].message)
            self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...', captured.records[2].message)

            self.assertEqual('		Processing "Channel Title Beta (10982)" Members and Group Profile Picture', captured.records[3].message)
            self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...', captured.records[4].message)

            self.assertEqual('		Processing "Channel Title Delta (10983)" Members and Group Profile Picture', captured.records[5].message)
            self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...', captured.records[6].message)

            self.assertEqual('		Processing "Channel Title Echo (10984)" Members and Group Profile Picture', captured.records[7].message)
            self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...', captured.records[8].message)

            self.assertEqual('		Processing "Channel Title Charlie (10985)" Members and Group Profile Picture', captured.records[9].message)
            self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...', captured.records[10].message)

            self.assertEqual('		Processing "Channel Title Fox (10989)" Members and Group Profile Picture', captured.records[11].message)
            self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...', captured.records[12].message)

    def test_run_download_groups_simulate_channel_participants_not_iterable_error(self):
        """Test Run Method for Scrap Telegram Groups - Simulates a ChannelParticipants Not Iterable Error."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock(side_effect=self.run_connect_side_effect)

        # Setup the Download Profile Photos Mockup
        telegram_client_mockup.download_profile_photo = mock.AsyncMock(side_effect=self.coroutine_downloadfile)

        telegram_client_mockup.iter_participants = mock.MagicMock(side_effect=TypeError("'ChannelParticipants' object is not subscriptable"))

        target: TelegramGroupScrapper = TelegramGroupScrapper()
        args: Dict = {
            'load_groups': True,
            'config': 'unittest_configfile.config',
            'refresh_profile_photos': True,
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

            # Check Logs
            self.assertEqual(15, len(captured.records))
            self.assertEqual('		Enumerating Groups', captured.records[0].message)
            self.assertEqual('		Processing "Channel Title Alpha (10981)" Members and Group Profile Picture', captured.records[1].message)
            self.assertEqual('			...Unable to Download Chat Participants due ChannelParticipants Restrictions...', captured.records[2].message)

            self.assertEqual('		Processing "Channel Title Beta (10982)" Members and Group Profile Picture', captured.records[3].message)
            self.assertEqual('			...Unable to Download Chat Participants due ChannelParticipants Restrictions...', captured.records[4].message)

            self.assertEqual('		Processing "Channel Title Delta (10983)" Members and Group Profile Picture', captured.records[5].message)
            self.assertEqual('			...Unable to Download Chat Participants due ChannelParticipants Restrictions...', captured.records[6].message)

            self.assertEqual('		Processing "Channel Title Echo (10984)" Members and Group Profile Picture', captured.records[7].message)
            self.assertEqual('			...Unable to Download Chat Participants due ChannelParticipants Restrictions...', captured.records[8].message)

            self.assertEqual('		Processing "Channel Title Charlie (10985)" Members and Group Profile Picture', captured.records[9].message)
            self.assertEqual('			...Unable to Download Chat Participants due ChannelParticipants Restrictions...', captured.records[10].message)

            self.assertEqual('		Processing "Channel Title Fox (10989)" Members and Group Profile Picture', captured.records[11].message)
            self.assertEqual('			...Unable to Download Chat Participants due ChannelParticipants Restrictions...', captured.records[12].message)

            self.assertEqual('		Processing "None (10999)" Members and Group Profile Picture', captured.records[13].message)
            self.assertEqual('			...Unable to Download Chat Participants due ChannelParticipants Restrictions...', captured.records[14].message)

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

        telegram_client_mockup.iter_participants = mock.MagicMock(
            return_value=async_generator_side_effect(base_users_mockup_data))

        target: TelegramGroupScrapper = TelegramGroupScrapper()
        args: Dict = {
            'load_groups': True,
            'config': 'unittest_configfile.config',
            'refresh_profile_photos': True,
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

            # Check Logs
            self.assertEqual(8, len(captured.records))
            self.assertEqual('		Enumerating Groups', captured.records[0].message)
            self.assertEqual('		Processing "Channel Title Alpha (10981)" Members and Group Profile Picture', captured.records[1].message)
            self.assertEqual('		Processing "Channel Title Beta (10982)" Members and Group Profile Picture', captured.records[2].message)
            self.assertEqual('		Processing "Channel Title Delta (10983)" Members and Group Profile Picture', captured.records[3].message)
            self.assertEqual('		Processing "Channel Title Echo (10984)" Members and Group Profile Picture', captured.records[4].message)
            self.assertEqual('		Processing "Channel Title Charlie (10985)" Members and Group Profile Picture', captured.records[5].message)
            self.assertEqual('		Processing "Channel Title Fox (10989)" Members and Group Profile Picture', captured.records[6].message)
            self.assertEqual('		Processing "None (10999)" Members and Group Profile Picture', captured.records[7].message)

        # Check all Groups in SQLlite DB
        all_groups = DbManager.SESSIONS['data'].execute(
            select(TelegramGroupOrmEntity)
        ).scalars().all()

        self.assertEqual(7, len(all_groups))

        self.assertTrue(all_groups[2].restricted)

        self.assertEqual('-81612359763615430348', all_groups[3].access_hash)
        self.assertEqual('2200278116', all_groups[3].constructor_id)
        self.assertEqual('cte', all_groups[3].group_username)
        self.assertEqual(
            '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',
            all_groups[3].photo_base64)
        self.assertEqual(5155552649748597242, all_groups[3].photo_id)
        self.assertEqual('test_run_connect.jpg', all_groups[3].photo_name)
        self.assertEqual('5526986587745', all_groups[3].source)
        self.assertEqual('Channel Title Echo', all_groups[3].title)

        self.assertIsNone(all_groups[5].photo_id)
        self.assertIsNone(all_groups[5].photo_name)
        self.assertIsNone(all_groups[5].photo_base64)

        # Check all Members in SQLlite DB
        all_members = DbManager.SESSIONS['data'].execute(
            select(TelegramUserOrmEntity)
        ).scalars().all()

        self.assertEqual(6, len(all_members))
        self.assertEqual('aghatarnuners', all_members[3].first_name)
        self.assertEqual(1351859319, all_members[3].id)

        self.assertTrue(all_members[5].is_bot)

        self.assertEqual('John', all_members[4].first_name)
        self.assertEqual('Snow', all_members[4].last_name)
        self.assertEqual('15894317355', all_members[4].phone_number)
        self.assertEqual('15894317355', all_members[4].phone_number)
        self.assertEqual('johnsnow55', all_members[4].username)
        self.assertTrue(all_members[4].is_self)

    def test_run_download_groups_disabled(self):
        """Test Run Method for Scrap Telegram Groups Disabled."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock(side_effect=self.run_connect_side_effect)

        # Setup the Download Profile Photos Mockup
        telegram_client_mockup.download_profile_photo = mock.AsyncMock(side_effect=self.coroutine_downloadfile)

        # Setup the IterParticipants Mockup
        async def async_generator_side_effect(items):
            for item in items:
                yield item

        telegram_client_mockup.iter_participants = mock.MagicMock(
            return_value=async_generator_side_effect(base_users_mockup_data))

        target: TelegramGroupScrapper = TelegramGroupScrapper()
        args: Dict = {
            'load_groups': False,
            'config': 'unittest_configfile.config',
            'refresh_profile_photos': True,
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
            self.assertEqual('\t\tModule is Not Enabled...', captured.records[0].message)

    def run_connect_side_effect(self, param):

        if isinstance(param, GetDialogsRequest):
            return base_groups_mockup_data

        raise Exception(type(param))

    async def coroutine_downloadfile(self, entity, file, download_big) -> str:

        # Copy Resources
        shutil.copyfile('resources/122761750_387013276008970_8208112669996447119_n.jpg',
                        '_data/resources/test_run_connect.jpg')

        # Return the Path
        return '_data/resources/test_run_connect.jpg'
