"""MP4 Media Handler."""

from typing import Dict, List, Optional

from telethon.tl.types import DocumentAttributeFilename, DocumentAttributeVideo, Message, MessageMediaDocument


class MediaMp4Handler:
    """MP4 Media Handler - video/mp4."""

    @staticmethod
    def handle_metadata(message: Message) -> Optional[Dict]:
        """Handle Media Metadata."""
        media: MessageMediaDocument = message.media
        fn_attr: List = [item for item in media.document.attributes if isinstance(item, DocumentAttributeFilename)]
        fn_attr_vid: List = [item for item in media.document.attributes if isinstance(item, DocumentAttributeVideo)]

        return {
            'file_name': fn_attr[0].file_name if len(fn_attr) > 0 else "unknow.mp4",
            'telegram_id': media.document.id,
            'extension': None,
            'height': fn_attr_vid[0].h if len(fn_attr_vid) > 0 else None,
            'width': fn_attr_vid[0].w if len(fn_attr_vid) > 0 else None,
            'date_time': media.document.date,
            'mime_type': media.document.mime_type,
            'size_bytes': media.document.size,
            'title': None,
            'name': None
            }
