"""Geo Media Handler."""

from typing import Dict, Optional

from telethon.tl.types import Message, MessageMediaGeo


class GeoMediaHandler:
    """Geo Media Handler."""

    @staticmethod
    def handle_metadata(message: Message) -> Optional[Dict]:
        """Handle Media Metadata."""
        # Get Media
        geo: MessageMediaGeo = message.geo

        # Create Data Dict
        return {
            'file_name': 'geo.bin',

            'telegram_id': None,
            'extension': None,
            'height': None,
            'width': None,
            'date_time': None,
            'mime_type': 'application/vnd.geo',
            'size_bytes': None,
            'title': f'{geo.lat}|{geo.long}',
            'name': None
            }
