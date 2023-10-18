"""Plain Text Media Handler."""
from __future__ import annotations

from typing import Dict, Optional

from telethon.tl.patched import Message
from telethon.tl.types import DocumentAttributeFilename, MessageMediaDocument


class TextPlainHandler:
    """Plain Text Media Handler - text/plain."""

    @staticmethod
    def handle_metadata(message: Message) -> Optional[Dict]:
        """Handle Media Metadata."""
        media: MessageMediaDocument = message.media
        return {
            'file_name':
                [item for item in message.media.document.attributes if isinstance(item, DocumentAttributeFilename)][
                    0].file_name,
            'telegram_id': media.document.id,
            'extension': None,
            'height': None,
            'width': None,
            'date_time': media.document.date,
            'mime_type': media.document.mime_type,
            'size_bytes': media.document.size,
            'title': None,
            'name': None,
        }
