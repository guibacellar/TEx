"""HTTP Navigation Manager Tests."""

import unittest
from typing import Dict
from configparser import ConfigParser

from OSIx.core.temp_file import TempFileHandler
from OSIx.modules.http_navigation_manager import HttpNavigationManagerHandler
from unittest.mock import patch


class HttpNavigationManagerHandlerTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('config.ini')

    def test_general(self):

        target: HttpNavigationManagerHandler = HttpNavigationManagerHandler()
        args: Dict = {'btc_wallet': 'WALLET_UUID'}
        data: Dict = {}

        target.run(
            config=self.config,
            args=args,
            data=data
        )

        # Validate data
        self.assertIsNotNone('WALLET_UUID', data['web_navigation']['user_agent'])

