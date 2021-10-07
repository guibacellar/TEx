"""Temp File Handle Tests."""

import unittest
from OSIx.core.temp_file import TempFileHandler


class TempFileHandlerTest(unittest.TestCase):

    def test_file_exist_not_found(self):
        self.assertFalse(TempFileHandler.file_exist('foofile.json'))

    def test_write_read_exists(self):

        TempFileHandler.write_file_text('utfile.json', 'ConTENt01')
        self.assertTrue(TempFileHandler.file_exist('utfile.json'))
        self.assertEqual('ConTENt01', ''.join(TempFileHandler.read_file_text('utfile.json')))
