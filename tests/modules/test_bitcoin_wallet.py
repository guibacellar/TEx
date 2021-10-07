"""Bitcoint Wallet Handler Tests."""

import unittest
from typing import Dict
from configparser import ConfigParser

from OSIx.core.dir_manager import DirectoryManagerUtils
from OSIx.core.temp_file import TempFileHandler
from OSIx.modules.bitcoin_wallet import BitcoinWalletInfoDownloader, BitcoinWalletTransactionsDownloader
from unittest.mock import patch


class BitcoinWalletInfoDownloaderTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('config.ini')

        DirectoryManagerUtils.ensure_dir_struct('data/')

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, content, status_code):
                self.content = content
                self.status_code = status_code

            def json(self):
                return self.json_data

        if kwargs['url'] == 'https://chain.api.btc.com/v3/address/WALLET_UUID':
            return MockResponse(b'{"data":{"address":"1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3","received":630608008,"sent":612982346,"balance":17625662,"tx_count":743,"unconfirmed_tx_count":0,"unconfirmed_received":0,"unconfirmed_sent":0,"unspent_tx_count":131,"first_tx":"27b8e738f2fbd93521fcc5dd2bde7253f1421747fd0dc4e5d66d6844d2349386","last_tx":"67ec78cf9b3fc3162ca96b66c314078a2b250a30209c6c8fa25eaf7db23c0127"},"err_code":0,"err_no":0,"message":"success","status":"success"}\n', 200)

        return None

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_general(self, mocked_get):

        target: BitcoinWalletInfoDownloader = BitcoinWalletInfoDownloader()
        args: Dict = {'btc_wallet': 'WALLET_UUID'}
        data: Dict = {}

        target.run(
            config=self.config,
            args=args,
            data=data
        )

        # Double Run
        target.run(
            config=self.config,
            args=args,
            data=data
        )

        # Validate data
        self.assertEqual('WALLET_UUID', data['bitcoin']['target_wallet'])

        # Validate Created File
        self.assertTrue(TempFileHandler.file_exist('bitcoin_wallet/WALLET_UUID_wallet.json'))

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_empty_wallet(self, mocked_get):

        target: BitcoinWalletInfoDownloader = BitcoinWalletInfoDownloader()
        args: Dict = {'btc_wallet': ''}
        data: Dict = {}

        target.run(
            config=self.config,
            args=args,
            data=data
        )

        # Validate data
        self.assertEqual('', data['bitcoin']['target_wallet'])


class BitcoinWalletTransactionsDownloaderTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('config.ini')

        DirectoryManagerUtils.ensure_dir_struct('data/')

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, content, status_code):
                self.content = content
                self.status_code = status_code

            def json(self):
                return self.json_data

        if kwargs['url'] == 'https://blockchain.info/rawaddr/WALLET_UUID?format=json&offset=0&limit=1000':

            with open('assets/bitcoin_wallet_transactions.json', 'rb') as file:
                return MockResponse(file.read(), 200)

        return None

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_general(self, mocked_get):

        target: BitcoinWalletTransactionsDownloader = BitcoinWalletTransactionsDownloader()
        args: Dict = {'btc_get_transactions': True}
        data: Dict = {
            'bitcoin':
                {
                    'target_wallet': 'WALLET_UUID'
                }
        }

        target.run(
            config=self.config,
            args=args,
            data=data
        )

        # Double Run
        with self.assertLogs() as captured:
            target.run(
                config=self.config,
                args=args,
                data=data
            )

            self.assertEqual(len(captured.records), 1)
            self.assertEqual('\t\tTarget File "bitcoin_wallet/WALLET_UUID_transactions.json" Alread Exists. Skipping...', captured.records[0].msg)

        # Validate Created File
        self.assertTrue(TempFileHandler.file_exist('bitcoin_wallet/WALLET_UUID_transactions.json'))

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_disabled(self, mocked_get):

        target: BitcoinWalletTransactionsDownloader = BitcoinWalletTransactionsDownloader()
        args: Dict = {'btc_get_transactions': False}
        data: Dict = {
            'bitcoin':
                {
                    'target_wallet': 'WALLET_UUID2'
                }
        }

        target.run(
            config=self.config,
            args=args,
            data=data
        )

        # Validate Not Created File
        self.assertFalse(TempFileHandler.file_exist('bitcoin_wallet/WALLET_UUID2_transactions.json'))

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_empty(self, mocked_get):
        target: BitcoinWalletTransactionsDownloader = BitcoinWalletTransactionsDownloader()
        args: Dict = {'btc_get_transactions': True}
        data: Dict = {
            'bitcoin':
                {
                    'target_wallet': ''
                }
        }

        with self.assertLogs() as captured:
            target.run(
                config=self.config,
                args=args,
                data=data
            )

            self.assertEqual(len(captured.records), 1)
            self.assertEqual('\t\tTarget BTC Wallet Empty.', captured.records[0].msg)
