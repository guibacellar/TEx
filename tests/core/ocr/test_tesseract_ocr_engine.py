"""Test the Tesseract OCR Engine."""

import unittest
from unittest import mock
from configparser import ConfigParser
from typing import Dict

from TEx.core.ocr.ocr_engine_base import OcrEngineBase
from TEx.core.ocr.tesseract_ocr_engine import TesseractOcrEngine
from tests.modules.common import TestsCommon


class TesseractOcrEngineTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    @mock.patch('TEx.core.ocr.tesseract_ocr_engine.tesseract')
    @mock.patch('TEx.core.ocr.tesseract_ocr_engine.os')
    def test_all(self, mocked_os_lib, mocked_tesseract):
        """Test Tesseract Engine."""

        # Configure Mock
        mocked_tesseract.image_to_string = mock.MagicMock()
        mocked_os_lib.path = mock.MagicMock()
        mocked_os_lib.path.exists = mock.MagicMock(return_value=True)

        # Run Setup
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}

        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Change Config Settings
        self.config['OCR.TESSERACT']['tesseract_cmd'] = '/folder/to/cmd/file'
        self.config['OCR.TESSERACT']['language'] = 'eng+osd'

        # Create Test Target
        target: OcrEngineBase = TesseractOcrEngine()

        # Call Configure
        target.configure(config=self.config['OCR.TESSERACT'])

        # Call Run
        target.run(file_path='/path/to/target/image')

        # Check Internal Behaviour
        self.assertEqual('/folder/to/cmd/file', mocked_tesseract.tesseract_cmd)
        mocked_tesseract.image_to_string.assert_called_once_with(
            '/path/to/target/image',
            lang='eng+osd'
        )

    def test_configure_without_config(self):
        """Test Config Method without Config."""

        # Create Test Target
        target: OcrEngineBase = TesseractOcrEngine()

        # Call Configure
        with self.assertRaises(AttributeError) as context:
            target.configure(config=None)

        self.assertEqual('No [OCR.TESSERACT] config found, but OCR type is "tesseract"', context.exception.args[0])

    def test_configure_tesseract_cmd_empty(self):
        """Test Config Method when Tesseract Command are Empty."""
        # Run Setup
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}

        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Change Config Settings
        self.config['OCR.TESSERACT']['tesseract_cmd'] = ''
        self.config['OCR.TESSERACT']['language'] = 'eng+osd'

        # Create Test Target
        target: OcrEngineBase = TesseractOcrEngine()

        # Call Configure
        with self.assertRaises(AttributeError) as context:
            target.configure(config=self.config['OCR.TESSERACT'])

        self.assertEqual('"tesseract_cmd" setting are no properly set, but OCR type is "tesseract"', context.exception.args[0])

    def test_configure_tesseract_cmd_not_found(self):
        """Test Config Method when Tesseract CMD are Not Found."""
        # Run Setup
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}

        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Change Config Settings
        self.config['OCR.TESSERACT']['tesseract_cmd'] = '/folder/to/cmd/file'
        self.config['OCR.TESSERACT']['language'] = 'eng+osd'

        # Create Test Target
        target: OcrEngineBase = TesseractOcrEngine()

        # Call Configure
        with self.assertRaises(AttributeError) as context:
            target.configure(config=self.config['OCR.TESSERACT'])

        self.assertEqual(f'Tesseract command cannot be found at "/folder/to/cmd/file"', context.exception.args[0])

    @mock.patch('TEx.core.ocr.tesseract_ocr_engine.tesseract')
    def test_run_ocr_file_not_found(self, mocked_tesseract):
        """Test Tesseract Engine 'run' method returning Empty Value due a File not Found."""

        # Configure Mock
        mocked_tesseract.image_to_string = mock.MagicMock(side_effect=Exception())

        # Create Test Target
        target: OcrEngineBase = TesseractOcrEngine()

        # Call Run
        self.assertEqual('', target.run(file_path='/path/to/target/image'))
