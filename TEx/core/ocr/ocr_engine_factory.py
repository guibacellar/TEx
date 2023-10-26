"""Factory Class for ORC Engines."""
from __future__ import annotations

from configparser import ConfigParser, SectionProxy
from typing import Optional

from TEx.core.ocr.dummy_ocr_engine import DummyOcrEngine
from TEx.core.ocr.ocr_engine_base import OcrEngineBase
from TEx.core.ocr.tesseract_ocr_engine import TesseractOcrEngine


class OcrEngineFactory:
    """Factory Class for ORC Engines."""

    @staticmethod
    def get_instance(config: ConfigParser) -> OcrEngineBase:
        """Configure the Notifier."""
        if not config.has_section('OCR'):
            return DummyOcrEngine()

        ocr_settings: SectionProxy = config['OCR']

        # Get Activation and Type Settings
        is_enabled: bool = ocr_settings.get('enabled', fallback='false') == 'true'
        if not is_enabled:
            return DummyOcrEngine()

        # Get Configurations
        ocr_type: str = ocr_settings.get('type', fallback='none')
        engine: OcrEngineBase
        ocr_engine_settings: Optional[SectionProxy]

        # Return Tesseract Engine
        if ocr_type == 'tesseract':
            engine = TesseractOcrEngine()
            ocr_engine_settings = config['OCR.TESSERACT']
        else:
            error_msg: str = f'Invalid OCR Type "{ocr_type}"'
            raise AttributeError(error_msg)

        # Configure Engine
        engine.configure(config=ocr_engine_settings)

        return engine
