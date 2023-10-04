"""Telethon Channel Entity Mapper."""
from typing import Dict

from telethon.tl.types import Channel


class TelethonChannelEntityMapper:
    """Telethon Channel Entity Mapper."""

    @staticmethod
    def to_database_dict(channel: Channel, target_phone_numer: str) -> Dict:
        """Map Telethon Channel to TeX Dict to Insert into DB."""
        # Build Model
        values: Dict = {
            'id': channel.id,
            'constructor_id': channel.CONSTRUCTOR_ID,
            'access_hash': str(channel.access_hash),
            'fake': getattr(channel, 'fake', False),
            'gigagroup': getattr(channel, 'gigagroup', False),
            'has_geo': getattr(channel, 'has_geo', False),
            'participants_count': getattr(channel, 'participants_count', 0),
            'restricted': getattr(channel, 'restricted', False),
            'scam': getattr(channel, 'scam', False),
            'group_username': getattr(channel, 'username', ''),
            'verified': getattr(channel, 'verified', False),
            'title': getattr(channel, 'title', ''),
            'source': target_phone_numer
            }

        return values
