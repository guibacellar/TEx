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
            'file_name': f'photo{message.file.ext}',
            'telegram_id': media.photo.id,
            'extension': message.file.ext,
            'height': message.file.height,
            'width': message.file.width,
            'date_time': media.photo.date,
            'mime_type': message.file.mime_type,
            'size_bytes': message.file.size,
            'title': None,
            'name': None
            }
