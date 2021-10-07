"""Gravatar Username Data Digger Tests."""

import unittest
from typing import Dict, List
from configparser import ConfigParser
import hashlib

from OSIx.modules.gravatar_username_data_digger import GravatarUsernameDataDigger, GravatarDataPrinter
from OSIx.modules.temp_file_manager import TempFileManager
from unittest import mock


class GravatarUsernameDataDiggerTest(unittest.TestCase):

    EXPECTED_NOTFOUND_MESSAGES: List = [
        '\t\tRunning...',
        '\t\tUsername Not Found.',
        '\t\tUsername Not Present.'
        ]

    EXPECTED_LAUREN_MESSAGES: List = [
        '\t\tRunning...',
        '\t\tGravatar ID......: 56f16c06cabf0c535af9a0a0855320f2',
        '\t\tUsername.........: laurentessmann',
        '\t\tFull Name........: LaurenTessmann',
        '\t\tProfile Picture..: http://1.gravatar.com/avatar/56f16c06cabf0c535af9a0a0855320f2?size=800',
        '\t\tLocation.........: Porto Alegre',
        '\t\tLinks............: 8', '\t\t\tWordPress (http://laurentessmann.wordpress.com/) > http://laurentessmann.wordpress.com/',
        '\t\t\tTwitter (http://twitter.com/laurentessmann) > http://twitter.com/laurentessmann',
        '\t\t\tFacebook (http://www.facebook.com/Lauzinhaaa) > http://www.facebook.com/Lauzinhaaa',
        '\t\t\tEmail (laurentessmann@hotmail.com) > laurentessmann@hotmail.com',
        '\t\t\tAIM (aim:goim?screenname=laurentessmann@aol.com) > laurentessmann@aol.com',
        '\t\t\tYahoo! (ymsgr:sendim?lauzinhatessmann@yahoo.com.br) > lauzinhatessmann@yahoo.com.br',
        '\t\t\tGTalk (lautessmann) > lautessmann',
        '\t\t\tSkype (skype:laurentessmann) > laurentessmann'
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
        target_file: str = f'assets/gravatar_responses/{hashlib.md5(args[0].encode("utf-8")).hexdigest()}.json'

        with open(target_file, 'r', encoding='utf-8') as file:
            return file.read()

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_laurentessmann_user(self, _mocked_download_text):

        target_1: GravatarUsernameDataDigger = GravatarUsernameDataDigger()
        target_2: GravatarDataPrinter = GravatarDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'laurentessmann'}}

        # First Run
        with self.assertLogs() as captured:
            target_1.run(config=self.config, args=args, data=data)
            target_2.run(config=self.config, args=args, data=data)

            # Check the Emitted Logs
            self.assertEqual(len(captured.records), len(GravatarUsernameDataDiggerTest.EXPECTED_LAUREN_MESSAGES))
            for ix in range(len(GravatarUsernameDataDiggerTest.EXPECTED_LAUREN_MESSAGES)):
                self.assertEqual(captured.records[ix].message, GravatarUsernameDataDiggerTest.EXPECTED_LAUREN_MESSAGES[ix])

        # Validated Basic Data
        self.assertEqual('56f16c06cabf0c535af9a0a0855320f2', data['gravatar']['laurentessmann']['gravatar_id'])
        self.assertEqual('http://1.gravatar.com/avatar/56f16c06cabf0c535af9a0a0855320f2?size=800', data['gravatar']['laurentessmann']['image'])
        self.assertEqual('laurentessmann', data['gravatar']['laurentessmann']['username'])
        self.assertEqual('LaurenTessmann', data['gravatar']['laurentessmann']['fullname'])
        self.assertEqual('Porto Alegre', data['gravatar']['laurentessmann']['location'])

        # Validate Links
        self.assertEqual(8, len(data['gravatar']['laurentessmann']['links']))
        self.assertEqual(data['gravatar']['laurentessmann']['links'][0], {'name': 'WordPress', 'full_target': 'http://laurentessmann.wordpress.com/', 'target': 'http://laurentessmann.wordpress.com/'})
        self.assertEqual(data['gravatar']['laurentessmann']['links'][4], {'name': 'AIM', 'full_target': 'aim:goim?screenname=laurentessmann@aol.com', 'target': 'laurentessmann@aol.com'})
        self.assertEqual(data['gravatar']['laurentessmann']['links'][7], {'name': 'Skype', 'full_target': 'skype:laurentessmann', 'target': 'laurentessmann'})

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_qualityrealtime_user(self, _mocked_download_text):

        target_1: GravatarUsernameDataDigger = GravatarUsernameDataDigger()
        target_2: GravatarDataPrinter = GravatarDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'qualityrealtime'}}

        # First Run
        target_1.run(config=self.config, args=args, data=data)
        target_2.run(config=self.config, args=args, data=data)

        # Validated Basic Data
        self.assertEqual('0550bce9df63578e81540306a6b976f0', data['gravatar']['qualityrealtime']['gravatar_id'])
        self.assertEqual('http://1.gravatar.com/avatar/0550bce9df63578e81540306a6b976f0?size=800', data['gravatar']['qualityrealtime']['image'])
        self.assertEqual('qualityrealtime', data['gravatar']['qualityrealtime']['username'])
        self.assertEqual('qualitybargain', data['gravatar']['qualityrealtime']['fullname'])
        self.assertEqual('global', data['gravatar']['qualityrealtime']['location'])

        # Validate Links
        self.assertEqual(8, len(data['gravatar']['qualityrealtime']['links']))
        self.assertEqual(data['gravatar']['qualityrealtime']['links'][0], {'name': 'Email', 'full_target': 'qualitybargain@mail.com', 'target': 'qualitybargain@mail.com'})
        self.assertEqual(data['gravatar']['qualityrealtime']['links'][1], {'name': 'AIM', 'full_target': 'aim:goim?screenname=qualitybargain', 'target': 'qualitybargain'})
        self.assertEqual(data['gravatar']['qualityrealtime']['links'][2], {'name': 'Yahoo!', 'full_target': 'ymsgr:sendim?qualitybargain', 'target': 'qualitybargain'})
        self.assertEqual(data['gravatar']['qualityrealtime']['links'][3], {'name': 'ICQ', 'full_target': 'aim:goim?screenname=qualitybargain', 'target': 'qualitybargain'})
        self.assertEqual(data['gravatar']['qualityrealtime']['links'][4], {'name': 'Jabber', 'full_target': 'qualitybargain', 'target': 'qualitybargain'})
        self.assertEqual(data['gravatar']['qualityrealtime']['links'][5], {'name': 'GTalk', 'full_target': 'qualitybargain', 'target': 'qualitybargain'})
        self.assertEqual(data['gravatar']['qualityrealtime']['links'][6], {'name': 'Skype', 'full_target': 'skype:qualitybargain', 'target': 'qualitybargain'})
        self.assertEqual(data['gravatar']['qualityrealtime']['links'][7], {'name': 'Work Phone', 'full_target': '2816528179', 'target': '2816528179'})

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_cliaoliveira_user(self, _mocked_download_text):

        target_1: GravatarUsernameDataDigger = GravatarUsernameDataDigger()
        target_2: GravatarDataPrinter = GravatarDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'cliaoliveira'}}

        # First Run
        target_1.run(config=self.config, args=args, data=data)
        target_2.run(config=self.config, args=args, data=data)

        # Validated Basic Data
        self.assertEqual('cf11a1cdf58e4161c4d1d6c8b767343a', data['gravatar']['cliaoliveira']['gravatar_id'])
        self.assertEqual('http://2.gravatar.com/avatar/cf11a1cdf58e4161c4d1d6c8b767343a?size=800', data['gravatar']['cliaoliveira']['image'])
        self.assertEqual('cliaoliveira', data['gravatar']['cliaoliveira']['username'])
        self.assertEqual('cliaoliveira', data['gravatar']['cliaoliveira']['fullname'])
        self.assertEqual('Rio de Janeiro', data['gravatar']['cliaoliveira']['location'])
        self.assertEqual('http://en.gravatar.com/cliaoliveira', data['gravatar']['cliaoliveira']['gravatar_url'])

        # Validate Links
        self.assertEqual(9, len(data['gravatar']['cliaoliveira']['links']))
        self.assertEqual(data['gravatar']['cliaoliveira']['links'][0], {'name': 'Twitter', 'full_target': 'http://twitter.com/CliaROSilva', 'target': 'http://twitter.com/CliaROSilva'})
        self.assertEqual(data['gravatar']['cliaoliveira']['links'][1], {'name': 'Facebook', 'full_target': 'http://facebook.com/regina.silva.102', 'target': 'http://facebook.com/regina.silva.102'})
        self.assertEqual(data['gravatar']['cliaoliveira']['links'][2], {'name': 'Flickr', 'full_target': 'http://flickr.com/photos/flickr.com/people/90250275@N08/', 'target': 'http://flickr.com/photos/flickr.com/people/90250275@N08/'})
        self.assertEqual(data['gravatar']['cliaoliveira']['links'][3], {'name': 'Tumblr', 'full_target': 'http://celia65os.tumblr.com/', 'target': 'http://celia65os.tumblr.com/'})
        self.assertEqual(data['gravatar']['cliaoliveira']['links'][4], {'name': 'Vimeo', 'full_target': 'http://http://vimeo.com/user18925311', 'target': 'http://http://vimeo.com/user18925311'})
        self.assertEqual(data['gravatar']['cliaoliveira']['links'][5], {'name': 'Yahoo!', 'full_target': 'http://profile.yahoo.com/PF4T4POSROAKNJFCOGJCT66ZIM', 'target': 'http://profile.yahoo.com/PF4T4POSROAKNJFCOGJCT66ZIM'})
        self.assertEqual(data['gravatar']['cliaoliveira']['links'][6], {'name': 'Email', 'full_target': 'celperfam6515@hotmail.com', 'target': 'celperfam6515@hotmail.com'})
        self.assertEqual(data['gravatar']['cliaoliveira']['links'][7], {'name': 'AIM', 'full_target': 'aim:goim?screenname=Identificador...', 'target': 'Identificador...'})
        self.assertEqual(data['gravatar']['cliaoliveira']['links'][8], {'name': 'Yahoo!', 'full_target': 'ymsgr:sendim?clia_oliveira@ymail.com', 'target': 'clia_oliveira@ymail.com'})

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_dpapa187_user(self, _mocked_download_text):

        target_1: GravatarUsernameDataDigger = GravatarUsernameDataDigger()
        target_2: GravatarDataPrinter = GravatarDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'dpapa187'}}

        # First Run
        target_1.run(config=self.config, args=args, data=data)
        target_2.run(config=self.config, args=args, data=data)

        # Validated Basic Data
        self.assertEqual('562c6023baa2c913746562023d42b81d', data['gravatar']['dpapa187']['gravatar_id'])
        self.assertEqual('http://2.gravatar.com/avatar/562c6023baa2c913746562023d42b81d?size=800', data['gravatar']['dpapa187']['image'])
        self.assertEqual('dpapa187', data['gravatar']['dpapa187']['username'])
        self.assertEqual('DPAPA\'s Living A Flip Flop Life!', data['gravatar']['dpapa187']['fullname'])
        self.assertEqual('Greece', data['gravatar']['dpapa187']['location'])
        self.assertEqual('http://en.gravatar.com/dpapa187', data['gravatar']['dpapa187']['gravatar_url'])

        # Validate Links
        self.assertEqual(6, len(data['gravatar']['dpapa187']['links']))
        self.assertEqual(data['gravatar']['dpapa187']['links'][0], {'name': 'WordPress', 'full_target': 'http://d-papa.com/', 'target': 'http://d-papa.com/'})
        self.assertEqual(data['gravatar']['dpapa187']['links'][1], {'name': 'Twitter', 'full_target': 'http://twitter.com/dpapaimc', 'target': 'http://twitter.com/dpapaimc'})
        self.assertEqual(data['gravatar']['dpapa187']['links'][2], {'name': 'Facebook', 'full_target': 'http://www.facebook.com/522315791', 'target': 'http://www.facebook.com/522315791'})
        self.assertEqual(data['gravatar']['dpapa187']['links'][3], {'name': 'Email', 'full_target': 'dpapaimc@gmail.com', 'target': 'dpapaimc@gmail.com'})
        self.assertEqual(data['gravatar']['dpapa187']['links'][4], {'name': 'AIM', 'full_target': 'aim:goim?screenname=www.facebook.com/dpapaimc', 'target': 'www.facebook.com/dpapaimc'})
        self.assertEqual(data['gravatar']['dpapa187']['links'][5], {'name': 'Skype', 'full_target': 'skype:dpapa187', 'target': 'dpapa187'})

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_radoalves_user(self, _mocked_download_text):

        target_1: GravatarUsernameDataDigger = GravatarUsernameDataDigger()
        target_2: GravatarDataPrinter = GravatarDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'radoalves'}}

        # First Run
        target_1.run(config=self.config, args=args, data=data)
        target_2.run(config=self.config, args=args, data=data)

        # Validated Basic Data
        self.assertEqual('8bbfe8ab2e5e96dc83d6365aa8983c84', data['gravatar']['radoalves']['gravatar_id'])
        self.assertEqual('http://1.gravatar.com/avatar/8bbfe8ab2e5e96dc83d6365aa8983c84?size=800', data['gravatar']['radoalves']['image'])
        self.assertEqual('radoalves', data['gravatar']['radoalves']['username'])
        self.assertEqual('Pastor Ricardo Alves', data['gravatar']['radoalves']['fullname'])
        self.assertEqual('Turmalina MG', data['gravatar']['radoalves']['location'])
        self.assertEqual('http://en.gravatar.com/radoalves', data['gravatar']['radoalves']['gravatar_url'])

        # Validate Links
        self.assertEqual(8, len(data['gravatar']['radoalves']['links']))
        self.assertEqual(data['gravatar']['radoalves']['links'][0], {'name': 'Facebook', 'full_target': 'http://www.facebook.com/100000365515365', 'target': 'http://www.facebook.com/100000365515365'})
        self.assertEqual(data['gravatar']['radoalves']['links'][1], {'name': 'Flickr', 'full_target': 'https://www.flickr.com/people/radoalves/', 'target': 'https://www.flickr.com/people/radoalves/'})
        self.assertEqual(data['gravatar']['radoalves']['links'][2], {'name': 'Email', 'full_target': 'radoalves@oi.com.br', 'target': 'radoalves@oi.com.br'})
        self.assertEqual(data['gravatar']['radoalves']['links'][3], {'name': 'AIM', 'full_target': 'aim:goim?screenname=radoalves', 'target': 'radoalves'})
        self.assertEqual(data['gravatar']['radoalves']['links'][4], {'name': 'Yahoo!', 'full_target': 'ymsgr:sendim?radoalves', 'target': 'radoalves'})
        self.assertEqual(data['gravatar']['radoalves']['links'][5], {'name': 'Jabber', 'full_target': 'radoalves@gmail.com', 'target': 'radoalves@gmail.com'})
        self.assertEqual(data['gravatar']['radoalves']['links'][6], {'name': 'Home Phone', 'full_target': '3891362174', 'target': '3891362174'})
        self.assertEqual(data['gravatar']['radoalves']['links'][7], {'name': 'Cell Phone', 'full_target': '3891362174', 'target': '3891362174'})

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_aldoafj_user(self, _mocked_download_text):

        target_1: GravatarUsernameDataDigger = GravatarUsernameDataDigger()
        target_2: GravatarDataPrinter = GravatarDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'aldoafj'}}

        # First Run
        target_1.run(config=self.config, args=args, data=data)
        target_2.run(config=self.config, args=args, data=data)

        # Validated Basic Data
        self.assertEqual('f7f811805cc4b31fcb2804b299169dfe', data['gravatar']['aldoafj']['gravatar_id'])
        self.assertEqual('http://0.gravatar.com/avatar/f7f811805cc4b31fcb2804b299169dfe?size=800', data['gravatar']['aldoafj']['image'])
        self.assertEqual('aldoafj', data['gravatar']['aldoafj']['username'])
        self.assertEqual('aldoramos', data['gravatar']['aldoafj']['fullname'])
        self.assertEqual('São Paulo', data['gravatar']['aldoafj']['location'])
        self.assertEqual('http://en.gravatar.com/aldoafj', data['gravatar']['aldoafj']['gravatar_url'])

        # Validate Links
        self.assertEqual(4, len(data['gravatar']['aldoafj']['links']))
        self.assertEqual(data['gravatar']['aldoafj']['links'][0], {'name': 'Facebook', 'full_target': 'https://www.facebook.com/app_scoped_user_id/10206617497810567/', 'target': 'https://www.facebook.com/app_scoped_user_id/10206617497810567/'})
        self.assertEqual(data['gravatar']['aldoafj']['links'][1], {'name': 'Tumblr', 'full_target': 'http://aldoafj-blog.tumblr.com/', 'target': 'http://aldoafj-blog.tumblr.com/'})
        self.assertEqual(data['gravatar']['aldoafj']['links'][2], {'name': 'Email', 'full_target': 'Identificador...gmail@', 'target': 'Identificador...gmail@'})
        self.assertEqual(data['gravatar']['aldoafj']['links'][3], {'name': 'AIM', 'full_target': 'aim:goim?screenname=Identificador...', 'target': 'Identificador...'})

    @mock.patch('OSIx.core.http_manager.HttpNavigationManager.get', side_effect=mocked_get)
    def test_run_notfound0x02_user(self, _mocked_download_text):
        target_1: GravatarUsernameDataDigger = GravatarUsernameDataDigger()
        target_2: GravatarDataPrinter = GravatarDataPrinter()
        args: Dict = {'username_print_result': True}
        data: Dict = {'username': {'target_username': 'notfound0x02'}}

        # First Run
        with self.assertLogs() as captured:
            target_1.run(config=self.config, args=args, data=data)
            target_2.run(config=self.config, args=args, data=data)

            # Check the Emitted Logs
            self.assertEqual(len(captured.records), len(GravatarUsernameDataDiggerTest.EXPECTED_NOTFOUND_MESSAGES))
            for ix in range(len(GravatarUsernameDataDiggerTest.EXPECTED_NOTFOUND_MESSAGES)):
                self.assertEqual(captured.records[ix].message, GravatarUsernameDataDiggerTest.EXPECTED_NOTFOUND_MESSAGES[ix])

        # Validated Basic Data
        self.assertIsNone(data['gravatar']['notfound0x02']['gravatar_id'])
        self.assertIsNone(data['gravatar']['notfound0x02']['image'])
        self.assertIsNone(data['gravatar']['notfound0x02']['username'])
        self.assertIsNone(data['gravatar']['notfound0x02']['fullname'])
        self.assertIsNone(data['gravatar']['notfound0x02']['location'])
        self.assertIsNone(data['gravatar']['notfound0x02']['gravatar_url'])

        # Validate Links
        self.assertEqual(0, len(data['gravatar']['notfound0x02']['links']))
