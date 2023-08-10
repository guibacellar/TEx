"""Telegram Connection Manager Tests."""

import asyncio
import unittest
from unittest import mock
from typing import Dict
from configparser import ConfigParser
from TEx.modules.telegram_connection_manager import TelegramConnector, TelegramDisconnector


class TelegramConnectorTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_run_connect(self):
        """Test Run Method with Telegram Server Connection."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock()
        started_telegram_client_mockup = mock.AsyncMock()

        telegram_client_mockup.start = mock.AsyncMock(return_value=started_telegram_client_mockup)
        telegram_client_mockup.is_user_authorized = mock.AsyncMock(return_value=True)

        """Run Test for Connection to Telegram Servers."""
        target: TelegramConnector = TelegramConnector()
        args: Dict = {
            'connect': True,
            'api_id': 'MyTestApiID',
            'api_hash': 'MyTestApiHash',
            'target_phone_number': 'MyTestPhoneNumber'
        }
        data: Dict = {}

        with mock.patch('TEx.modules.telegram_connection_manager.TelegramClient', return_value=telegram_client_mockup):
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
                self.assertEqual(2, len(captured.records))
                self.assertEqual('		User Authorized on Telegram: True', captured.records[1].message)

        # Validate Mock Calls
        telegram_client_mockup.start.assert_awaited_once_with(phone='MyTestPhoneNumber')

        # Validate Data Result Dict
        self.assertEqual('MyTestApiID', data['telegram_connection']['api_id'])
        self.assertEqual('MyTestApiHash', data['telegram_connection']['api_hash'])
        self.assertEqual('MyTestPhoneNumber', data['telegram_connection']['phone_number'])
        self.assertEqual(telegram_client_mockup, data['telegram_client'])

    def test_run_reuse(self):
        """Test Run Method with Reused Connection."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock()
        started_telegram_client_mockup = mock.AsyncMock()

        telegram_client_mockup.start = mock.AsyncMock(return_value=started_telegram_client_mockup)
        telegram_client_mockup.is_user_authorized = mock.AsyncMock(return_value=False)

        """Run Test for Connection to Telegram Servers."""
        target: TelegramConnector = TelegramConnector()
        args: Dict = {
            'connect': False,
            'load_groups': True,
            'download_messages': False
        }
        data: Dict = {
            'telegram_connection': {
                'api_id': 'MyTestApiID2',
                'api_hash': 'MyTestApiHash2',
                'target_phone_number': 'MyTestPhoneNumber2',
                'session_code': '1AZWarxxBu1K7H_xk4-uACJYt3R_zyEPdZGd6t6nyAIxH8r6yVxMrMBP2xRyKhQAT3-KyR2T4BpLicQR6_54yvYatWV0WN2nAZMpyHGdJ-GXCyeiDxhAf4vFWb_eaw8fN4FeNPygq6VGQxOs56H_yO47zVYrwF4OZNBfe8rZISG2YLer43zwJ8fCySlrf8pswx0huRC-ntDWMNrR60_B61SX3_tQYcA1OGujHc6SjCGINxnOqltL0L359iG-CdDvde2-ZWAPLYutR1Q4T48h_GEI_vHhB0DPob9NsQyrLR6QuYO5UnhgbJIs2Fs0ysJfkGBAHsYnFPzDfpKCusC8ubl1phtcyTqg='
            }
        }

        with mock.patch('TEx.modules.telegram_connection_manager.TelegramClient', return_value=telegram_client_mockup):
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
                self.assertEqual(1, len(captured.records))
                self.assertEqual('		User Authorized on Telegram: False', captured.records[0].message)

        # Validate Mock Calls
        telegram_client_mockup.start.assert_awaited_once_with(phone='MyTestPhoneNumber2')

        # Validate Data Result Dict
        self.assertEqual('MyTestApiID2', data['telegram_connection']['api_id'])
        self.assertEqual('MyTestApiHash2', data['telegram_connection']['api_hash'])
        self.assertEqual('MyTestPhoneNumber2', data['telegram_connection']['phone_number'])
        self.assertEqual(telegram_client_mockup, data['telegram_client'])

    def test_run_reuse_without_authentication(self):
        """Test Run Method with Reused Connection without Previous Connection."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock()
        started_telegram_client_mockup = mock.AsyncMock()

        telegram_client_mockup.start = mock.AsyncMock(return_value=started_telegram_client_mockup)
        started_telegram_client_mockup.is_user_authorized = mock.AsyncMock(return_value=False)

        """Run Test for Connection to Telegram Servers."""
        target: TelegramConnector = TelegramConnector()
        args: Dict = {
            'connect': False,
            'load_groups': True,
            'download_messages': False
        }
        data: Dict = {
            'telegram_connection': {
            }
        }

        with mock.patch('TEx.modules.telegram_connection_manager.TelegramClient', return_value=telegram_client_mockup):
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
                self.assertEqual(1, len(captured.records))
                self.assertEqual('\t\tNot Authenticated on Telegram. Please use the "connect" command.', captured.records[0].message)


class TelegramDisconnectorTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_run_disconnect(self):
        """Test Run Method with Telegram Server Disconnection."""

        # Setup Mock
        telegram_client_mockup = mock.AsyncMock()
        telegram_client_mockup.disconnect = mock.AsyncMock()

        """Run Test for Connection to Telegram Servers."""
        target: TelegramDisconnector = TelegramDisconnector()
        args: Dict = {}
        data: Dict = {'telegram_client': telegram_client_mockup}

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            target.run(
                config=self.config,
                args=args,
                data=data
            )
        )

        # Validate Mock Calls
        telegram_client_mockup.disconnect.assert_awaited_once()
        self.assertFalse('telegram_client' in data)
