"""Echo OCR Engine for Unittest only."""
from configparser import SectionProxy
from typing import Optional

from TEx.core.ocr.ocr_engine_base import OcrEngineBase


class UnitTestEchoOcrEngine(OcrEngineBase):
    """Dummy OCR Engine."""

    def __init__(self, echo_message: Optional[str]) -> None:
        """Echo OCR Engine for Unittest only."""
        super().__init__()
        self.echo: Optional[str] = echo_message

    def configure(self, config: Optional[SectionProxy]) -> None:
        """Configure Dummy Engine."""
        pass

    def run(self, file_path: str) -> Optional[str]:
        """Do Nothing."""
        return self.echo
