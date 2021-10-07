"""Username Scanner Tests."""
import json
import os
import unittest
from typing import Dict
from configparser import ConfigParser
from uuid import uuid4
import hashlib

import requests.exceptions

from OSIx.modules.temp_file_manager import TempFileManager
from OSIx.modules.username_handler import UsernameScanner
from unittest import mock


class UsernameScannerTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        print(os.path.dirname('../config.ini'))
        self.config.read(os.path.join(os.path.dirname(__file__), '../config.ini'))

        # Purge Temp File
        TempFileManager().run(
            config=self.config,
            args={'purge_temp_files': True},
            data={}
        )

    def mocked_get_future_result(*args, **kwargs):
        class MockResponse:
            def __init__(self, text=None, status_code=None, url=None):
                self.text = text
                self.status_code = status_code
                self.elapsed = 8
                self.url = url

            def result(self):

                target_file: str = f'tests/assets/username_responses/{hashlib.md5(self.url.encode("utf-8")).hexdigest()}.json'

                if self.url == 'http://forum.3dnews.ru/member.php?username=marcos':
                    raise requests.exceptions.HTTPError()

                elif self.url == 'https://www.7cups.com/@marcos':
                    raise requests.exceptions.ProxyError()

                elif self.url == 'https://about.me/marcos':
                    raise requests.exceptions.ConnectionError()

                elif self.url == 'https://www.alik.cz/u/marcos':
                    raise requests.exceptions.Timeout()

                elif self.url == 'https://discussions.apple.com/profile/marcos':
                    raise requests.exceptions.RequestException()

                if not os.path.exists(target_file):
                    return MockResponse(text="", status_code=404)

                with open(target_file, 'r', encoding='utf-8') as file:

                    json_data: Dict = json.loads(file.read())

                    return MockResponse(
                        text=json_data['text'],
                        status_code=int(json_data['status'])
                    )

        return MockResponse(url=args[4])

    def test_run(self):

        target: UsernameScanner = UsernameScanner()
        random_username: str = uuid4().hex
        args: Dict = {'username': random_username, 'username_allow_nsfw_scan': True, 'username_enable_dump_file': True, 'username_scan': True, 'username_print_result': True, 'username_show_all': False}
        data: Dict = {}

        with open('assets/username_handler_do_scan_mocked_data.json') as file:
            mock_content: str = file.read()

        with mock.patch('OSIx.modules.username_handler.UsernameScanner._UsernameScanner__do_scan', return_value=json.loads(mock_content)) as patched_do_scan:

            # First Run
            target.run(
                config=self.config,
                args=args,
                data=data
            )

            # Assert Mock Called
            patched_do_scan.assert_called_once_with(
                target_username=random_username,
                target_sites=mock.ANY,
                config=self.config
            )

            # Double Run
            target.run(
                config=self.config,
                args=args,
                data=data
            )

        # Validate the Username are Included in Data
        self.assertEqual(random_username, data['username']['target_username'])

        # Check Data Dict
        self.assertTrue(len(data['username']['detected']) > 100)

        root_node: Dict = data['username']['detected']['GitHub']['status']

        self.assertEqual('guibacellar@gmail.com', root_node['username'])
        self.assertEqual('GitHub', root_node['site_name'])
        self.assertEqual('https://www.github.com/guibacellar@gmail.com', root_node['site_url_user'])
        self.assertEqual('Illegal', root_node['status'])
        self.assertIsNone(root_node['query_time'])
        self.assertIsNone(root_node['context'])

        # Check Created File
        self.assertTrue(os.path.exists(f'data/export/username_{random_username}.csv'))

    @mock.patch('OSIx.modules.username_handler.UsernameScanner._UsernameScanner__get_future', side_effect=mocked_get_future_result)
    def test_run_mock_future(self, mocked_get_future):

        target: UsernameScanner = UsernameScanner()
        args: Dict = {
            'username': 'marcos',
            'username_allow_nsfw_scan': True,
            'username_enable_dump_file': True,
            'username_print_result': True,
            'username_show_all': True,
            'username_scan': True
        }
        data: Dict = {}

        # First Run
        target.run(
            config=self.config,
            args=args,
            data=data
        )
