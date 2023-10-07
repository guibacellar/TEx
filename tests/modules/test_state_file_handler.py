"""State File Handler Tests."""
import asyncio
import unittest
from configparser import ConfigParser
from typing import Dict

from TEx.modules.state_file_handler import LoadStateFileHandler, SaveStateFileHandler
from tests.modules.common import TestsCommon


class StateFileHandlerTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('config.ini')

        TestsCommon.basic_test_setup()

    def test_run(self):

        target_load: LoadStateFileHandler = LoadStateFileHandler()
        target_save: SaveStateFileHandler = SaveStateFileHandler()
        args: Dict = {'config': 'unittest_configfile.config'}
        save_data: Dict = {'demo': 1, 'internals': {'panic': False}}

        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=save_data)

        loop = asyncio.get_event_loop()

        loop.run_until_complete(
            target_save.run(
                config=self.config,
                args=args,
                data=save_data
            )
        )

        load_data: Dict = {}
        loop.run_until_complete(
            target_load.run(
                config=self.config,
                args=args,
                data=load_data
            )
        )

        self.assertEqual(load_data, save_data)

