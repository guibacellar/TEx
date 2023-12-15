"""Do Nothing Media Handler."""
from __future__ import annotations

from typing import Dict, Optional

from telethon.tl.patched import Message


class DoNothingHandler:
    """Do Nothing Media Handler."""

    @staticmethod
    def handle_metadata(message: Message) -> Optional[Dict]:
        """Handle Media Metadata."""
        return None
