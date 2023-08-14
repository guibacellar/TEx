"""State File Handler Tests."""
import asyncio
import logging
import logging.config

import unittest
from typing import Dict
from configparser import ConfigParser

from TEx.core.dir_manager import DirectoryManagerUtils
from TEx.database.db_initializer import DbInitializer
from TEx.modules.execution_configuration_handler import ExecutionConfigurationHandler
from TEx.modules.state_file_handler import SaveStateFileHandler, LoadStateFileHandler


class StateFileHandlerTest(unittest.TestCase):

    def setUp(self) -> None:
        logging.config.fileConfig('logging.conf')

        self.config = ConfigParser()
        self.config.read('config.ini')

        DirectoryManagerUtils.ensure_dir_struct('_data/')

        DbInitializer.init(data_path='_data/')

    def test_run(self):

        execution_configuration_loader: ExecutionConfigurationHandler = ExecutionConfigurationHandler()
        target_load: LoadStateFileHandler = LoadStateFileHandler()
        target_save: SaveStateFileHandler = SaveStateFileHandler()
        args: Dict = {'config': 'unittest_configfile.config'}
        save_data: Dict = {'demo': 1}

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            execution_configuration_loader.run(
                config=self.config,
                args=args,
                data=save_data
            )
        )

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

