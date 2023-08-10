"""Telethon Channel Entity Mapper."""
from typing import Dict

from telethon.tl.types import Channel


class TelethonChannelEntiyMapper:
    """Telethon Channel Entity Mapper."""

    @staticmethod
    def to_database_dict(channel: Channel, target_phone_numer: str) -> Dict:
        """Map Telethon Channel to TeX Dict to Insert into DB."""
        # Build Model
        values: Dict = {
            'id': channel.id,
            'constructor_id': channel.CONSTRUCTOR_ID,
            'access_hash': str(channel.access_hash),
            'fake': channel.fake,
            'gigagroup': getattr(channel, 'gigagroup', False),
            'has_geo': getattr(channel, 'has_geo', False),
            'participants_count': channel.participants_count,
            'restricted': channel.restricted,
            'scam': channel.scam,
            'group_username': channel.username,
            'verified': channel.verified,
            'title': channel.title,
            'source': target_phone_numer
            }

        return values
