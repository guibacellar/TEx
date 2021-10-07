"""State File Handler Tests."""

import logging
import logging.config

import unittest
import uuid
from typing import Dict
from configparser import ConfigParser

from OSIx.core.dir_manager import DirectoryManagerUtils
from OSIx.modules.state_file_handler import SaveStateFileHandler, LoadStateFileHandler


class StateFileHandlerTest(unittest.TestCase):

    def setUp(self) -> None:
        logging.config.fileConfig('logging.conf')

        self.config = ConfigParser()
        self.config.read('config.ini')

        DirectoryManagerUtils.ensure_dir_struct('data/')

    def test_run(self):

        target_load: LoadStateFileHandler = LoadStateFileHandler()
        target_save: SaveStateFileHandler = SaveStateFileHandler()
        args: Dict = {'job_name': uuid.uuid4().hex}
        save_data: Dict = {'demo': 1}

        target_save.run(
            config=self.config,
            args=args,
            data=save_data
        )

        load_data: Dict = {}
        target_load.run(
            config=self.config,
            args=args,
            data=load_data
        )

        self.assertEqual(load_data, save_data)

