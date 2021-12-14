"""Input Args Handler Tests."""

import sys
import asyncio
import unittest
from typing import Dict
from configparser import ConfigParser
from TEx.modules.input_args_handler import InputArgsHandler


class InputArgsHandlerTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_report_commands_complete(self):

        sys.argv = [
            '__main__.py',
            'report',
            '--phone_number', '+98765123456',
            '--order_desc',
            '--limit_days', '8',
            '--filter', 'filter1, "Filter 2", Filter3',
            '--report_folder', 'reports/ut01',
            '--around_messages', '7',
            '--group_id', '99,5,78,56987',
            '--data_path', '_data'
            ]

        target: InputArgsHandler = InputArgsHandler()
        args: Dict = {}
        data: Dict = {}

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            target.run(
                config=self.config,
                args=args,
                data=data
            )
        )

        self.assertEqual('+98765123456', args['target_phone_number'])
        self.assertTrue(args['order_desc'])
        self.assertEqual('filter1, "Filter 2", Filter3', args['filter'])
        self.assertEqual(8, int(args['limit_days']))
        self.assertEqual('reports/ut01', args['report_folder'])
        self.assertEqual(7, int(args['around_messages']))
        self.assertEqual('99,5,78,56987', args['group_id'])

    def test_report_commands_default(self):

        sys.argv = [
            '__main__.py',
            'report',
            '--phone_number', '+98765123456',
            '--data_path', '_data'
        ]

        target: InputArgsHandler = InputArgsHandler()
        args: Dict = {}
        data: Dict = {}

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            target.run(
                config=self.config,
                args=args,
                data=data
            )
        )

        self.assertEqual('+98765123456', args['target_phone_number'])
        self.assertFalse(args['order_desc'])
        self.assertIsNone(args['filter'])
        self.assertEqual(3650, int(args['limit_days']))
        self.assertEqual('reports', args['report_folder'])
        self.assertEqual(1, int(args['around_messages']))
        self.assertEqual('*', args['group_id'])
