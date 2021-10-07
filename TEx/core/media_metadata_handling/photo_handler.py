"""Photo Media Handler."""

from typing import Dict, Optional

from telethon.tl.types import Message, MessageMediaPhoto


class PhotoMediaHandler:
    """Photo Media Handler."""

    @staticmethod
    def handle_metadata(message: Message) -> Optional[Dict]:
        """Handle Media Metadata."""
        media: MessageMediaPhoto = message.media

        return {
            'file_name': None,
            'telegram_id': media.photo.id,
            'extension': None,
            'height': None,
            'width': None,
            'date_time': media.photo.date,
            'mime_type': None,
            'size_bytes': None,
            'title': None,
            'name': None,
            'b64_content': None
            }
