"""Steam Username Data Digger Tests."""
import json
import os
import shutil
import sys
import unittest
from typing import Dict
from configparser import ConfigParser
from uuid import uuid4
import hashlib

import requests.exceptions

from OSIx.core.temp_file import TempFileHandler
from OSIx.modules.github_username_data_digger import GithubUsernameDataDigger
from OSIx.modules.temp_file_manager import TempFileManager
from OSIx.modules.steam_username_data_digger import SteamUsernameDataDigger, SteamIdFinderDataDigger, SteamDataPrinter
from unittest import mock


class SteamUsernameDataDiggerTest(unittest.TestCase):

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
        target_file: str = f'assets/steam_responses/{hashlib.md5(args[0].encode("utf-8")).hexdigest()}.json'

        with open(target_file, 'r', encoding='utf-8') as file:
            return file.read()

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_marcus_user(self, _mocked_download_text):

        target_1: SteamUsernameDataDigger = SteamUsernameDataDigger()
        target_2: SteamIdFinderDataDigger = SteamIdFinderDataDigger()
        target_3: SteamDataPrinter = SteamDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'marcus'}}

        # First Run
        target_1.run(config=self.config, args=args, data=data)
        target_2.run(config=self.config, args=args, data=data)
        target_3.run(config=self.config, args=args, data=data)

        self.assertEqual('STEAM_0:0:288072', data['steam']['marcus']['steam_id'])
        self.assertEqual('76561197960841872', data['steam']['marcus']['steam_id_64_dec'])
        self.assertEqual('11000010008ca90', data['steam']['marcus']['steam_id_64_hex'])
        self.assertEqual('[U:1:576144]', data['steam']['marcus']['steam_id_3'])
        self.assertEqual('Public', data['steam']['marcus']['profile_state'])
        self.assertEqual('September 16th, 2003', data['steam']['marcus']['profile_creation_data'])
        self.assertEqual('_AgainstAllOdds_', data['steam']['marcus']['username'])
        self.assertEqual('Marcus Schebiel', data['steam']['marcus']['fullname'])
        self.assertEqual('Kaufbeuren, Bayern, Germany', data['steam']['marcus']['location'])
        self.assertEqual('https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/avatars/ac/acdab7c604bf1e502fa8ae79d004d0b7298eec69_full.jpg', data['steam']['marcus']['profile_pic'])

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_notfound0x02_user(self, _mocked_download_text):

        target_1: SteamUsernameDataDigger = SteamUsernameDataDigger()
        target_2: SteamIdFinderDataDigger = SteamIdFinderDataDigger()
        target_3: SteamDataPrinter = SteamDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'notfound0x02'}}

        # First Run
        target_1.run(config=self.config, args=args, data=data)
        target_2.run(config=self.config, args=args, data=data)
        target_3.run(config=self.config, args=args, data=data)

        self.assertIsNone(data['steam']['notfound0x02']['steam_id'])
        self.assertIsNone(data['steam']['notfound0x02']['steam_id_64_dec'])
        self.assertIsNone(data['steam']['notfound0x02']['steam_id_64_hex'])
        self.assertIsNone(data['steam']['notfound0x02']['steam_id_3'])
        self.assertIsNone(data['steam']['notfound0x02']['profile_state'])
        self.assertIsNone(data['steam']['notfound0x02']['profile_creation_data'])
        self.assertIsNone(data['steam']['notfound0x02']['username'])
        self.assertIsNone(data['steam']['notfound0x02']['fullname'])
        self.assertIsNone(data['steam']['notfound0x02']['location'])
        self.assertIsNone(data['steam']['notfound0x02']['profile_pic'])

    def test_run_without_username(self):

        target_1: SteamUsernameDataDigger = SteamUsernameDataDigger()
        target_2: SteamIdFinderDataDigger = SteamIdFinderDataDigger()
        target_3: SteamDataPrinter = SteamDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': ''}}

        # First Run
        target_1.run(config=self.config, args=args, data=data)
        target_2.run(config=self.config, args=args, data=data)
        target_3.run(config=self.config, args=args, data=data)

        self.assertFalse('steam' in data)
