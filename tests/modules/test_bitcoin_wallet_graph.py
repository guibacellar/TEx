"""Bitcoin Wallet Graph Generator Tests."""

import shutil
import os
import unittest
from typing import Dict
from configparser import ConfigParser

from OSIx.core.dir_manager import DirectoryManagerUtils
from OSIx.core.temp_file import TempFileHandler
from OSIx.modules.bitcoin_wallet_graph import BitcoinWalletGraphGenerator
from unittest.mock import patch


class BitcoinWalletGraphGeneratorTest(unittest.TestCase):

    def setUp(self) -> None:

        self.config = ConfigParser()
        self.config.read('config.ini')

        DirectoryManagerUtils.ensure_dir_struct('data/')
        DirectoryManagerUtils.ensure_dir_struct('data/export/')

    def test_general_gephi(self):

        # Copy the Asset file to data folder
        with open(os.path.abspath(os.path.join(os.getcwd(), 'assets/1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3_transactions.json')), 'r') as file:
            TempFileHandler.write_file_text(
                path='bitcoin_wallet/1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3ut_transactions.json',
                content=''.join(file.readlines())
            )

        target: BitcoinWalletGraphGenerator = BitcoinWalletGraphGenerator()
        args: Dict = {'export_btc_transactions_as_gephi': True}
        data: Dict = {
            'bitcoin': {
                'target_wallet': '1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3ut'
            }
        }

        target.run(
            config=self.config,
            args=args,
            data=data
        )

        # Validate Generated Files
        self.assertTrue(os.path.exists('data/export/btc_wallet_all_1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3ut.gexf'))
        self.assertTrue(os.path.exists('data/export/btc_wallet_outputs_1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3ut.gexf'))
        self.assertTrue(os.path.exists('data/export/btc_wallet_inputs_1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3ut.gexf'))

    def test_general_graphml(self):

        # Copy the Asset file to data folder
        with open(os.path.abspath(os.path.join(os.getcwd(), 'assets/1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3_transactions.json')), 'r') as file:
            TempFileHandler.write_file_text(
                path='bitcoin_wallet/1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3ut_transactions.json',
                content=''.join(file.readlines())
            )

        target: BitcoinWalletGraphGenerator = BitcoinWalletGraphGenerator()
        args: Dict = {'export_btc_transactions_as_graphml': True, 'export_btc_transactions_as_gephi': False}
        data: Dict = {
            'bitcoin': {
                'target_wallet': '1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3ut'
            }
        }

        target.run(
            config=self.config,
            args=args,
            data=data
        )

        # Validate Generated Files
        self.assertTrue(os.path.exists('data/export/btc_wallet_all_1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3ut.graphml'))
        self.assertTrue(os.path.exists('data/export/btc_wallet_outputs_1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3ut.graphml'))
        self.assertTrue(os.path.exists('data/export/btc_wallet_inputs_1Mn8mS3w5VGGRUYmoamJTGAhmQj7JTq8e3ut.graphml'))
