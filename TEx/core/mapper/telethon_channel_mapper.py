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
            'fake': channel.fake if channel.fake else False,
            'gigagroup': channel.gigagroup if channel.gigagroup else False,
            'has_geo': channel.has_geo if channel.has_geo else False,
            'participants_count': channel.participants_count if channel.participants_count else 0,
            'restricted': channel.restricted if channel.restricted else False,
            'scam': channel.scam if channel.scam else False,
            'group_username': channel.username if channel.username else '',
            'verified': channel.verified if channel.verified else False,
            'title': channel.title if channel.title else '',
            'source': target_phone_numer
            }

        return values
