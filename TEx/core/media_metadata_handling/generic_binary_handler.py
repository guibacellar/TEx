"""Generic Binary Media Handler."""

from typing import Dict, List, Optional

from telethon.tl.types import DocumentAttributeFilename, Message, MessageMediaDocument


class GenericBinaryMediaHandler:
    """Generic Binary Media Handler."""

    @staticmethod
    def handle_metadata(message: Message) -> Optional[Dict]:
        """Handle Media Metadata."""
        media: MessageMediaDocument = message.media
        fn_attr: List = [item for item in media.document.attributes if isinstance(item, DocumentAttributeFilename)]

        return {
            'file_name': fn_attr[0].file_name if len(fn_attr) > 0 else "unknow.bin",
            'telegram_id': media.document.id,
            'extension': None,
            'height': None,
            'width': None,
            'date_time': media.document.date,
            'mime_type': media.document.mime_type,
            'size_bytes': media.document.size,
            'title': None,
            'name': None
            }
