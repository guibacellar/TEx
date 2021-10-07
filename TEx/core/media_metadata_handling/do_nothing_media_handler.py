"""Do Nothing Media Handler."""
from typing import Dict, Optional

from telethon.tl.types import Message


class DoNothingHandler:
    """Do Nothing Media Handler."""

    @staticmethod
    def handle_metadata(message: Message) -> Optional[Dict]:  # pylint: disable=W0613
        """Handle Media Metadata."""
        return None
