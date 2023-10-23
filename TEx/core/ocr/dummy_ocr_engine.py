"""Dummy OCR Engine."""
from __future__ import annotations

from configparser import SectionProxy
from typing import Optional

from TEx.core.ocr.ocr_engine_base import OcrEngineBase


class DummyOcrEngine(OcrEngineBase):
    """Dummy OCR Engine."""

    def __init__(self) -> None:
        """Initialize Dummy Engine."""
        super().__init__()

    def configure(self, config: Optional[SectionProxy]) -> None:
        """Configure Dummy Engine."""

    def run(self, file_path: str) -> Optional[str]:
        """Do Nothing."""
        return None
