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
            self._extracted_from_test_run_download_groups_simulate_channel_private_error_25(
                target, args, data, captured
            )

    # TODO Rename this here and in `test_run_download_groups_simulate_channel_private_error`
    def _extracted_from_test_run_download_groups_simulate_channel_private_error_25(self, target, args, data, captured):
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
        self.assertEqual('		Processing "Channel Title Alpha (10981)" Members and Group Profile Picture',
                         captured.records[1].message)
        self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...',
                         captured.records[2].message)

        self.assertEqual('		Processing "Channel Title Beta (10982)" Members and Group Profile Picture',
                         captured.records[3].message)
        self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...',
                         captured.records[4].message)

        self.assertEqual('		Processing "Channel Title Delta (10983)" Members and Group Profile Picture',
                         captured.records[5].message)
        self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...',
                         captured.records[6].message)

        self.assertEqual('		Processing "Channel Title Echo (10984)" Members and Group Profile Picture',
                         captured.records[7].message)
        self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...',
                         captured.records[8].message)

        self.assertEqual('		Processing "Channel Title Charlie (10985)" Members and Group Profile Picture',
                         captured.records[9].message)
        self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...',
                         captured.records[10].message)

        self.assertEqual('		Processing "Channel Title Fox (10989)" Members and Group Profile Picture',
                         captured.records[11].message)
        self.assertEqual('			...Unable to Download Chat Participants due Private Chat Restrictions...',
                         captured.records[12].message)

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
            self._extracted_from_test_run_download_groups_simulate_peer_channel_restrictions_error_25(
                target, args, data, captured
            )

    # TODO Rename this here and in `test_run_download_groups_simulate_peer_channel_restrictions_error`
    def _extracted_from_test_run_download_groups_simulate_peer_channel_restrictions_error_25(self, target, args, data,
                                                                                             captured):
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
        self.assertEqual('		Processing "Channel Title Alpha (10981)" Members and Group Profile Picture',
                         captured.records[1].message)
        self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...',
                         captured.records[2].message)

        self.assertEqual('		Processing "Channel Title Beta (10982)" Members and Group Profile Picture',
                         captured.records[3].message)
        self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...',
                         captured.records[4].message)

        self.assertEqual('		Processing "Channel Title Delta (10983)" Members and Group Profile Picture',
                         captured.records[5].message)
        self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...',
                         captured.records[6].message)

        self.assertEqual('		Processing "Channel Title Echo (10984)" Members and Group Profile Picture',
                         captured.records[7].message)
        self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...',
                         captured.records[8].message)

        self.assertEqual('		Processing "Channel Title Charlie (10985)" Members and Group Profile Picture',
                         captured.records[9].message)
        self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...',
                         captured.records[10].message)

        self.assertEqual('		Processing "Channel Title Fox (10989)" Members and Group Profile Picture',
                         captured.records[11].message)
        self.assertEqual('			...Unable to Download Chat Participants due PerChannel Restrictions...',
                         captured.records[12].message)

    def test_run_download_groups_simulate_channel_participants_not_iterable_error(self):
        """Test Run Method for Scrap Telegram Groups - Simulates a ChannelParticipants Not Iterable Error."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock(side_effect=self.run_connect_side_effect)

        # Setup the Download Profile Photos Mockup
        telegram_client_mockup.download_profile_photo = mock.AsyncMock(side_effect=self.coroutine_downloadfile)

        telegram_client_mockup.iter_participants = mock.MagicMock(
            side_effect=TypeError("'ChannelParticipants' object is not subscriptable"))

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
            self._extracted_from_test_run_download_groups_simulate_channel_participants_not_iterable_error_26(
                target, args, data, captured
            )

    # TODO Rename this here and in `test_run_download_groups_simulate_channel_participants_not_iterable_error`
    def _extracted_from_test_run_download_groups_simulate_channel_participants_not_iterable_error_26(self, target, args,
                                                                                                     data, captured):
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
        self.assertEqual('		Processing "Channel Title Alpha (10981)" Members and Group Profile Picture',
                         captured.records[1].message)
        self.assertEqual(
            '			...Unable to Download Chat Participants due ChannelParticipants Restrictions...',
            captured.records[2].message)

        self.assertEqual('		Processing "Channel Title Beta (10982)" Members and Group Profile Picture',
                         captured.records[3].message)
        self.assertEqual(
            '			...Unable to Download Chat Participants due ChannelParticipants Restrictions...',
            captured.records[4].message)

        self.assertEqual('		Processing "Channel Title Delta (10983)" Members and Group Profile Picture',
                         captured.records[5].message)
        self.assertEqual(
            '			...Unable to Download Chat Participants due ChannelParticipants Restrictions...',
            captured.records[6].message)

        self.assertEqual('		Processing "Channel Title Echo (10984)" Members and Group Profile Picture',
                         captured.records[7].message)
        self.assertEqual(
            '			...Unable to Download Chat Participants due ChannelParticipants Restrictions...',
            captured.records[8].message)

        self.assertEqual('		Processing "Channel Title Charlie (10985)" Members and Group Profile Picture',
                         captured.records[9].message)
        self.assertEqual(
            '			...Unable to Download Chat Participants due ChannelParticipants Restrictions...',
            captured.records[10].message)

        self.assertEqual('		Processing "Channel Title Fox (10989)" Members and Group Profile Picture',
                         captured.records[11].message)
        self.assertEqual(
            '			...Unable to Download Chat Participants due ChannelParticipants Restrictions...',
            captured.records[12].message)

        self.assertEqual('		Processing "None (10999)" Members and Group Profile Picture',
                         captured.records[13].message)
        self.assertEqual(
            '			...Unable to Download Chat Participants due ChannelParticipants Restrictions...',
            captured.records[14].message)

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
            self.assertEqual('		Processing "Channel Title Alpha (10981)" Members and Group Profile Picture',
                             captured.records[1].message)
            self.assertEqual('		Processing "Channel Title Beta (10982)" Members and Group Profile Picture',
                             captured.records[2].message)
            self.assertEqual('		Processing "Channel Title Delta (10983)" Members and Group Profile Picture',
                             captured.records[3].message)
            self.assertEqual('		Processing "Channel Title Echo (10984)" Members and Group Profile Picture',
                             captured.records[4].message)
            self.assertEqual('		Processing "Channel Title Charlie (10985)" Members and Group Profile Picture',
                             captured.records[5].message)
            self.assertEqual('		Processing "Channel Title Fox (10989)" Members and Group Profile Picture',
                             captured.records[6].message)
            self.assertEqual('		Processing "None (10999)" Members and Group Profile Picture',
                             captured.records[7].message)

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
