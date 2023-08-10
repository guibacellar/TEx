"""Web Image Media Handler."""

from typing import Dict, List, Optional

from telethon.tl.types import DocumentAttributeFilename, DocumentAttributeImageSize, Message, MessageMediaDocument


class WebImageStickerHandler:
    """Web Image Media Handler - image/webp."""

    @staticmethod
    def handle_metadata(message: Message) -> Optional[Dict]:
        """Handle Media Metadata."""
        media: MessageMediaDocument = message.media

        fn_attr: List = [item for item in message.media.document.attributes if isinstance(item, DocumentAttributeFilename)]

        if not fn_attr or len(fn_attr) == 0:
            return None

        return {
            'file_name': fn_attr[0].file_name,
            'telegram_id': media.document.id,
            'extension': None,
            'height': [item for item in message.media.document.attributes if isinstance(item, DocumentAttributeImageSize)][0].h,
            'width': [item for item in message.media.document.attributes if isinstance(item, DocumentAttributeImageSize)][0].w,
            'date_time': media.document.date,
            'mime_type': media.document.mime_type,
            'size_bytes': media.document.size,
            'title': None,
            'name': None
            }
