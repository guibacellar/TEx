"""Base Class for OCR Engine."""
from __future__ import annotations

import abc
from configparser import SectionProxy
from typing import Optional


class OcrEngineBase:
    """Base Class for OCR Engine."""

    def __init__(self) -> None:
        """Initialize Base Class."""

    @abc.abstractmethod
    def configure(self, config: Optional[SectionProxy]) -> None:
        """Configure Abstract Method."""

    @abc.abstractmethod
    def run(self, file_path: str) -> Optional[str]:
        """Extract Text from Image."""
