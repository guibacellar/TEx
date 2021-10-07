"""GitHub Username Data Digger Tests."""

import unittest
from typing import Dict
from configparser import ConfigParser
import hashlib

from OSIx.modules.github_username_data_digger import GithubUsernameDataDigger, GithubDataPrinter
from OSIx.modules.temp_file_manager import TempFileManager
from unittest import mock


class GithubUsernameDataDiggerTest(unittest.TestCase):

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
        target_file: str = f'assets/github_responses/{hashlib.md5(args[0].encode("utf-8")).hexdigest()}.json'

        with open(target_file, 'r', encoding='utf-8') as file:
            return file.read()

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_elephant_user(self, _mocked_download_text):

        target_1: GithubUsernameDataDigger = GithubUsernameDataDigger()
        target_2: GithubDataPrinter = GithubDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'elephant'}}

        # First Run
        target_1.run(config=self.config, args=args, data=data)
        target_2.run(config=self.config, args=args, data=data)

        # Validated Basic Data
        self.assertEqual('https://avatars.githubusercontent.com/u/176842?v=4', data['github']['elephant']['profile_pic'])
        self.assertEqual('Jonathan Suchland', data['github']['elephant']['fullname'])
        self.assertEqual('elephant', data['github']['elephant']['nickname'])
        self.assertEqual('Seattle, WA', data['github']['elephant']['location'])
        self.assertEqual('http://jonathansuchland.com/', data['github']['elephant']['website'])
        self.assertEqual('176842', data['github']['elephant']['account_id'])
        self.assertEqual(None, data['github']['elephant']['bio'])

        # Validate Repositories
        self.assertEqual(11, len(data['github']['elephant']['repos']))
        self.assertEqual(data['github']['elephant']['repos'][2], {'name': 'elastic', 'description': 'Elasticsearch client for Go.', 'url': '/elephant/elastic', 'type': 'fork'})
        self.assertEqual(data['github']['elephant']['repos'][7], {'name': 'jquery-ui', 'description': 'The official jQuery user interface library.', 'url': '/elephant/jquery-ui', 'type': 'fork'})
        self.assertEqual(data['github']['elephant']['repos'][10], {'name': 'Catnap', 'description': 'Quickly create a RESTful web server from any PHP object.', 'url': '/elephant/Catnap', 'type': 'owner'})

        # Validate Followers
        self.assertEqual(13, len(data['github']['elephant']['followers']))
        self.assertEqual(data['github']['elephant']['followers'][0], {'name': '', 'username': 'parth-jani', 'url': '/parth-jani'})
        self.assertEqual(data['github']['elephant']['followers'][4], {'name': 'Navori Digital signage software', 'username': 'navori', 'url': '/navori'})
        self.assertEqual(data['github']['elephant']['followers'][9], {'name': 'Jimmy Odom', 'username': 'MnkyPwz', 'url': '/MnkyPwz'})

        # Validate Following
        self.assertEqual(6, len(data['github']['elephant']['following']))
        self.assertEqual(data['github']['elephant']['following'][1], {'name': 'Jay Aniceto', 'username': 'jayncoke', 'url': '/jayncoke'})
        self.assertEqual(data['github']['elephant']['following'][3], {'name': 'Jonathan Soeder', 'username': 'datapimp', 'url': '/datapimp'})
        self.assertEqual(data['github']['elephant']['following'][5], {'name': 'Harper Reed', 'username': 'harperreed', 'url': '/harperreed'})

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_john_user(self, _mocked_download_text):

        target_1: GithubUsernameDataDigger = GithubUsernameDataDigger()
        target_2: GithubDataPrinter = GithubDataPrinter()

        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'john'}}

        # First Run
        target_1.run(config=self.config, args=args, data=data)
        target_2.run(config=self.config, args=args, data=data)

        # Validated Basic Data
        self.assertEqual('https://avatars.githubusercontent.com/u/1668?v=4', data['github']['john']['profile_pic'])
        self.assertEqual('John McGrath', data['github']['john']['fullname'])
        self.assertEqual('john', data['github']['john']['nickname'])
        self.assertEqual('San Francisco, CA', data['github']['john']['location'])
        self.assertEqual('https://twitter.com/wordie', data['github']['john']['website'])
        self.assertEqual('1668', data['github']['john']['account_id'])
        self.assertEqual('I\'m on the sustainability team at AWS, and prior to that co-founded Entelo. Interested in renewable energy, journalism, startups, and democracy.', data['github']['john']['bio'])

        # Validate Repositories
        self.assertEqual(30, len(data['github']['john']['repos']))
        self.assertEqual(data['github']['john']['repos'][0], {'name': 'geocoder', 'description': 'Complete Ruby geocoding solution.', 'url': '/john/geocoder', 'type': 'fork'})
        self.assertEqual(data['github']['john']['repos'][5], {'name': 'daily-numbers', 'description': None, 'url': '/john/daily-numbers', 'type': 'owner'} )
        self.assertEqual(data['github']['john']['repos'][27], {'name': 'wrinkle', 'description': 'Moves content through space and time.', 'url': '/john/wrinkle', 'type': 'owner'})

        # Validate Followers
        self.assertEqual(50, len(data['github']['john']['followers']))
        self.assertEqual(data['github']['john']['followers'][2], {'name': 'Gupakg', 'username': 'Gupakg', 'url': '/Gupakg'})
        self.assertEqual(data['github']['john']['followers'][13], {'name': '', 'username': 'anupworks', 'url': '/anupworks'})
        self.assertEqual(data['github']['john']['followers'][25], {'name': '', 'username': 'jlsjefferson', 'url': '/jlsjefferson'})

        # Validate Following
        self.assertEqual(48, len(data['github']['john']['following']))
        self.assertEqual(data['github']['john']['following'][0], {'name': '', 'username': 'conslacksf', 'url': '/conslacksf'})
        self.assertEqual(data['github']['john']['following'][14], {'name': 'Linus Torvalds', 'username': 'torvalds', 'url': '/torvalds'})
        self.assertEqual(data['github']['john'] ['following'][47], {'name': 'André Arko', 'username': 'indirect', 'url': '/indirect'})

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_notfounduser001_user(self, _mocked_download_text):

        target_1: GithubUsernameDataDigger = GithubUsernameDataDigger()
        target_2: GithubDataPrinter = GithubDataPrinter()

        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'notfounduser001'}}

        # First Run
        with self.assertLogs() as captured:
            target_1.run(config=self.config, args=args, data=data)
            target_2.run(config=self.config, args=args, data=data)

        self.assertEqual(len(captured.records), 3)
        self.assertEqual(f'\t\tUsername Not Found.', captured.records[1].msg)

        # Validated Basic Data
        self.assertTrue('github' in data)
        self.assertTrue('notfounduser001' in data['github'])
        self.assertIsNone(data['github']['notfounduser001']['profile_pic'])
        self.assertIsNone(data['github']['notfounduser001']['fullname'])
        self.assertIsNone(data['github']['notfounduser001']['nickname'])
        self.assertIsNone(data['github']['notfounduser001']['bio'])
        self.assertIsNone(data['github']['notfounduser001']['location'])
        self.assertIsNone(data['github']['notfounduser001']['website'])
        self.assertIsNone(data['github']['notfounduser001']['account_id'])
        self.assertEqual(0, len(data['github']['notfounduser001']['repos']))
        self.assertEqual(0, len(data['github']['notfounduser001']['followers']))
        self.assertEqual(0, len(data['github']['notfounduser001']['following']))
