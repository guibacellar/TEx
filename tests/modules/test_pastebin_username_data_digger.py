"""Pastebin Username Data Digger Tests."""

import unittest
from typing import Dict, List
from configparser import ConfigParser
import hashlib

from OSIx.modules.pastebin_username_data_digger import PastebinUsernameDataDigger, PastebinDataPrinter
from OSIx.modules.temp_file_manager import TempFileManager
from unittest import mock


class PastebinUsernameDataDiggerTest(unittest.TestCase):

    EXPECTED_SUCCESS_MESSAGES: List = [
         '\t\tRunning...', '\t\tUsername.................: John',
         '\t\tCreated at...............: Thursday 26th of March 2015 06:22:30 PM CDT',
         '\t\tViews Count..............: 10614', '\t\tUsers Pastes Views Count.: 27229',
         '\t\tProfile Picture..........: https://pastebin.com/cache/img/7/23/22/1692844.jpg',
         '\t\tN. Public Pastes.........: 18',
         '\t\t\t[PS4] WW2 1.11 Huds (May 1st, 2019 ) at https://pastebin.com/YRCYk8EG',
         '\t\t\t[PS4] WW2 1.11 Addresses & Offsets (Mar 31st, 2019 ) at https://pastebin.com/3nY9CZ74',
         '\t\t\tWW2 PS4 Weapon Indices (Jun 8th, 2018 ) at https://pastebin.com/GTPFwtwH',
         '\t\t\tWW2 SP Function Labeler (Jun 2nd, 2018 ) at https://pastebin.com/XGR1jeLA',
         '\t\t\tAll PS4 error codes (Oct 22nd, 2017 ) at https://pastebin.com/3mf08dxg',
         '\t\t\t[GTA] Weapons (Mar 28th, 2017 ) at https://pastebin.com/bvHPd6N0',
         '\t\t\t[GTA] Radar Icons? (Mar 28th, 2017 ) at https://pastebin.com/219DW0wS',
         '\t\t\t[GTA] Particle effects? (Mar 28th, 2017 ) at https://pastebin.com/qCqwZDmp',
         '\t\t\t[GTA] Colors (Mar 28th, 2017 ) at https://pastebin.com/9Kgr1LLb',
         '\t\t\t[GTA] Rockstar Online Services URLs (Mar 28th, 2017 ) at https://pastebin.com/8ZiSSyeg',
         '\t\t\t[GTA] In-game websites (Mar 28th, 2017 ) at https://pastebin.com/39w8MeGx',
         '\t\t\t[GTA] Some mangled symbols (Mar 28th, 2017 ) at https://pastebin.com/4pwFC4Qi',
         '\t\t\t[GTA] Precached? strings (Mar 28th, 2017 ) at https://pastebin.com/YYeCRM7w',
         '\t\t\t[GTA] TriggerScriptEvent - cleaned up (Dec 21st, 2017 ) at https://pastebin.com/kWKZcshX',
         '\t\t\tx86 Menu Base (Oct 3rd, 2015 ) at https://pastebin.com/ptK7efRN',
         '\t\t\tIL .NET Menu Base (Sep 23rd, 2015 ) at https://pastebin.com/uCyFFUdr',
         '\t\t\tF# Menu Base (Sep 17th, 2015 ) at https://pastebin.com/hHVEp0Xd',
         '\t\t\tTimer Class (Jul 15th, 2016 ) at https://pastebin.com/W0rc9ApQ'
        ]

    EXPECTED_NOT_FOUND_MESSAGES: List = [
        '\t\tRunning...',
        '\t\tUsername Not Found.',
        '\t\tUsername Not Present.'
        ]

    EXPECTED_DISABLED_MESSAGES: List = [
        '\t\tUsername Not Provided. Skipping...',
        '\t\tUsername Not Provided. Skipping...'
        ]

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('config.ini')

        # Purge Temp File
        TempFileManager().run(
            config=self.config,
            args={'purge_temp_files': True},
            data={}
        )

    def mocked_get(*args, **kwargs):
        target_file: str = f'assets/pastebin_responses/{hashlib.md5(args[0].encode("utf-8")).hexdigest()}.json'

        with open(target_file, 'r', encoding='utf-8') as file:
            return file.read()

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_john_user(self, _mocked_download_text):

        target_1: PastebinUsernameDataDigger = PastebinUsernameDataDigger()
        target_2: PastebinDataPrinter = PastebinDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'john'}}

        # First Run
        with self.assertLogs() as captured:
            target_1.run(config=self.config, args=args, data=data)
            target_2.run(config=self.config, args=args, data=data)

            # Check the Emitted Logs
            self.assertEqual(len(captured.records), len(PastebinUsernameDataDiggerTest.EXPECTED_SUCCESS_MESSAGES))
            for ix in range(len(PastebinUsernameDataDiggerTest.EXPECTED_SUCCESS_MESSAGES)):
                self.assertEqual(captured.records[ix].message, PastebinUsernameDataDiggerTest.EXPECTED_SUCCESS_MESSAGES[ix])

        # Validated Basic Data
        self.assertEqual('John', data['pastebin']['john']['username'])
        self.assertEqual('Thursday 26th of March 2015 06:22:30 PM CDT', data['pastebin']['john']['created_at'])
        self.assertEqual(10614, data['pastebin']['john']['views_count'])
        self.assertEqual(27229, data['pastebin']['john']['all_views_count'])
        self.assertEqual('https://pastebin.com/cache/img/7/23/22/1692844.jpg', data['pastebin']['john']['image'])

        # Validate Public Pastes
        self.assertEqual(18, len(data['pastebin']['john']['public_pastes']))
        self.assertEqual(data['pastebin']['john']['public_pastes'][0], {'title': '[PS4] WW2 1.11 Huds', 'short_url': '/YRCYk8EG', 'full_url': 'https://pastebin.com/YRCYk8EG', 'date': 'May 1st, 2019 ', 'expires_at': 'Never', 'views_count': 587})
        self.assertEqual(data['pastebin']['john']['public_pastes'][2], {'title': 'WW2 PS4 Weapon Indices', 'short_url': '/GTPFwtwH', 'full_url': 'https://pastebin.com/GTPFwtwH', 'date': 'Jun 8th, 2018 ', 'expires_at': 'Never', 'views_count': 290})
        self.assertEqual(data['pastebin']['john']['public_pastes'][9], {'title': '[GTA] Rockstar Online Services URLs', 'short_url': '/8ZiSSyeg', 'full_url': 'https://pastebin.com/8ZiSSyeg', 'date': 'Mar 28th, 2017 ', 'expires_at': 'Never', 'views_count': 245})
        self.assertEqual(data['pastebin']['john']['public_pastes'][17], {'title': 'Timer Class', 'short_url': '/W0rc9ApQ', 'full_url': 'https://pastebin.com/W0rc9ApQ', 'date': 'Jul 15th, 2016 ', 'expires_at': 'Never', 'views_count': 1459})

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_notfound_user(self, _mocked_download_text):

        target_1: PastebinUsernameDataDigger = PastebinUsernameDataDigger()
        target_2: PastebinDataPrinter = PastebinDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'notfound0x02'}}

        # First Run
        with self.assertLogs() as captured:
            target_1.run(config=self.config, args=args, data=data)
            target_2.run(config=self.config, args=args, data=data)

            # Check the Emitted Logs
            self.assertEqual(len(captured.records), len(PastebinUsernameDataDiggerTest.EXPECTED_NOT_FOUND_MESSAGES))
            for ix in range(len(PastebinUsernameDataDiggerTest.EXPECTED_NOT_FOUND_MESSAGES)):
                self.assertEqual(captured.records[ix].message, PastebinUsernameDataDiggerTest.EXPECTED_NOT_FOUND_MESSAGES[ix])

        # Validated Basic Data
        self.assertIsNone(data['pastebin']['notfound0x02']['username'])
        self.assertIsNone(data['pastebin']['notfound0x02']['created_at'])
        self.assertIsNone(data['pastebin']['notfound0x02']['views_count'])
        self.assertIsNone(data['pastebin']['notfound0x02']['all_views_count'])
        self.assertIsNone(data['pastebin']['notfound0x02']['image'])
        self.assertEqual(0, len(data['pastebin']['notfound0x02']['public_pastes']))

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_disabled(self, _mocked_download_text):

        target_1: PastebinUsernameDataDigger = PastebinUsernameDataDigger()
        target_2: PastebinDataPrinter = PastebinDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': ''}}

        # First Run
        with self.assertLogs() as captured:
            target_1.run(config=self.config, args=args, data=data)
            target_2.run(config=self.config, args=args, data=data)

            # Check the Emitted Logs
            self.assertEqual(len(captured.records), len(PastebinUsernameDataDiggerTest.EXPECTED_DISABLED_MESSAGES))
            for ix in range(len(PastebinUsernameDataDiggerTest.EXPECTED_DISABLED_MESSAGES)):
                self.assertEqual(captured.records[ix].message, PastebinUsernameDataDiggerTest.EXPECTED_DISABLED_MESSAGES[ix])

        # Validated Basic Data
        self.assertFalse('pastebin' in data)


