"""Sticker Media Handler."""

from typing import Dict, List, Optional

from telethon.tl.types import DocumentAttributeFilename, DocumentAttributeImageSize, Message, MessageMediaDocument


class MediaStickerHandler:
    """Sticker Media Handler - application/x-tgsticker."""

    @staticmethod
    def handle_metadata(message: Message) -> Optional[Dict]:
        """Handle Media Metadata."""
        media: MessageMediaDocument = message.media
        fn_attr_img: List = [item for item in media.document.attributes if isinstance(item, DocumentAttributeImageSize)]

        return {
            'file_name': [item for item in message.media.document.attributes if isinstance(item, DocumentAttributeFilename)][0].file_name,
            'telegram_id': media.document.id,
            'extension': None,
            'height': fn_attr_img[0].h if len(fn_attr_img) > 0 else None,
            'width': fn_attr_img[0].w if len(fn_attr_img) > 0 else None,
            'date_time': media.document.date,
            'mime_type': media.document.mime_type,
            'size_bytes': media.document.size,
            'title': None,
            'name': None
            }
