"""Tesseract OCR Engine."""
from __future__ import annotations

import logging
import os
from configparser import SectionProxy
from typing import Optional, cast

from pytesseract import pytesseract as tesseract

from TEx.core.ocr.ocr_engine_base import OcrEngineBase

logger = logging.getLogger('TelegramExplorer')


class TesseractOcrEngine(OcrEngineBase):
    """Tesseract OCR Engine."""

    def __init__(self) -> None:
        """Initialize Discord Notifier."""
        super().__init__()
        self.cmd: str = ''
        self.language: str = ''

    def configure(self, config: Optional[SectionProxy]) -> None:
        """Configure the Notifier."""
        if not config:
            error_msg_config: str = 'No [OCR.TESSERACT] config found, but OCR type is "tesseract"'
            raise AttributeError(error_msg_config)

        self.cmd = config.get('tesseract_cmd', fallback='')
        self.language = config.get('language', fallback='eng')

        # Check if Tesseract CMD property are set
        if self.cmd == '':
            error_msg_cmd: str = '"tesseract_cmd" setting are no properly set, but OCR type is "tesseract"'
            raise AttributeError(error_msg_cmd)

        # Check if Tesseract CMD can be Found
        if not os.path.exists(self.cmd):
            error_msg_path: str = f'Tesseract command cannot be found at "{self.cmd}"'
            raise AttributeError(error_msg_path)

        # Configure Tesseract Engine
        tesseract.tesseract_cmd = self.cmd

    def run(self, file_path: str) -> Optional[str]:
        """Run Tesseract Engine and Return Detected Text."""
        try:

            if not os.path.exists(file_path):
                return ''

            return cast(str, tesseract.image_to_string(file_path, lang=self.language))

        except Exception as ex:
            logger.exception(msg='OCR Fail', exc_info=ex)

            return ''
