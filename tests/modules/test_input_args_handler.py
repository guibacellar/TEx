"""Directory Manager Tests."""

import sys
import unittest
from typing import Dict
from configparser import ConfigParser
from OSIx.modules.input_args_handler import InputArgsHandler

class InputArgsHandlerTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_jobname(self):

        sys.argv = [
            'C:/projects/OSIx/OSIx.py',
            '--job_name', 'job_insta_only'
            ]

        target: InputArgsHandler = InputArgsHandler()
        args: Dict = {}
        data: Dict = {}

        target.run(
            config=self.config,
            args=args,
            data=data
        )

        self.assertEqual('job_insta_only', args['job_name'])
        self.assertFalse(args['purge_temp_files'])
