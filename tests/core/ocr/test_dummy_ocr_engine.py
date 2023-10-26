"""Test the Dummy OCR Engine."""

import unittest

from TEx.core.ocr.dummy_ocr_engine import DummyOcrEngine
from TEx.core.ocr.ocr_engine_base import OcrEngineBase


class DummyOcrEngineTest(unittest.TestCase):

    def test_all(self):
        """Test Dummy Engine."""

        target: OcrEngineBase = DummyOcrEngine()
        target.configure(config=None)
        self.assertIsNone(target.run(file_path='/folder/path'))
