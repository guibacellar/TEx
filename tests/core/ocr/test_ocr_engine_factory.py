"""OcrEngineFactory Tests."""

import unittest
from unittest import mock
from configparser import ConfigParser
from typing import Dict

from TEx.core.ocr.dummy_ocr_engine import DummyOcrEngine
from TEx.core.ocr.ocr_engine_base import OcrEngineBase
from TEx.core.ocr.ocr_engine_factory import OcrEngineFactory
from TEx.core.ocr.tesseract_ocr_engine import TesseractOcrEngine
from tests.modules.common import TestsCommon


class OcrEngineFactoryTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    @mock.patch('TEx.core.ocr.tesseract_ocr_engine.os')
    def test_get_instance_tesseract(self, mocked_os_lib):
        """Test get_instance_method returning Tesseract Engine."""

        # Call Test Target Method
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}

        # Configure Mock
        mocked_os_lib.path = mock.MagicMock()
        mocked_os_lib.path.exists = mock.MagicMock(return_value=True)

        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        self.config['OCR']['enabled'] = 'true'
        self.config['OCR']['type'] = 'tesseract'

        self.config['OCR.TESSERACT']['tesseract_cmd'] = '/folder/file'
        self.config['OCR.TESSERACT']['language'] = 'eng+osd'

        h_result: OcrEngineBase = OcrEngineFactory.get_instance(self.config)
        self.assertTrue(isinstance(h_result, TesseractOcrEngine))

    def test_get_instance_no_ocr_config(self):
        """Test get_instance_method without OCR Setting on config file."""

        # Call Test Target Method
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}

        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        self.config.remove_section('OCR')
        self.config.remove_section('TESSERACT')

        h_result: OcrEngineBase = OcrEngineFactory.get_instance(self.config)
        self.assertTrue(isinstance(h_result, DummyOcrEngine))

    def test_get_instance_disabled_ocr_engine(self):
        """Test get_instance_method with OCR engine disabled on config file."""

        # Call Test Target Method
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}

        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        self.config['OCR']['enabled'] = 'false'
        self.config.remove_section('TESSERACT')

        h_result: OcrEngineBase = OcrEngineFactory.get_instance(self.config)
        self.assertTrue(isinstance(h_result, DummyOcrEngine))

    def test_get_instance_without_engine_ocr_engine(self):
        """Test get_instance_method with OCR engine enabled but without engine settings on config file."""

        # Call Test Target Method
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}

        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        self.config['OCR']['enabled'] = 'true'
        del self.config['OCR']['type']
        self.config.remove_section('TESSERACT')

        with self.assertRaises(AttributeError) as context:
            OcrEngineFactory.get_instance(self.config)
