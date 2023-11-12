"""Telethon Channel Entity Mapper."""
from typing import Dict, Union

from telethon.tl.types import Channel, Chat, User


class TelethonChannelEntityMapper:
    """Telethon Channel Entity Mapper."""

    @staticmethod
    def to_database_dict(entity: Union[Chat, Channel, User], target_phone_numer: str) -> Dict:
        """Map Telethon Entity to TEx Dict to Insert into DB."""
        # Build Model

        # Common Props
        values: Dict = {
            'id': entity.id,
            'constructor_id': entity.CONSTRUCTOR_ID,
            'source': target_phone_numer
        }

        # Apply Specific Mappers
        if isinstance(entity, Channel):
            values.update(TelethonChannelEntityMapper.__map_channel(entity))

        elif isinstance(entity, Chat):
            values.update(TelethonChannelEntityMapper.__map_chat(entity))

        elif isinstance(entity, User):
            values.update(TelethonChannelEntityMapper.__map_user(entity))

        return values

    @staticmethod
    def __map_channel(entity: Channel) -> Dict:
        """Map Telethon Channel to TEx Dict to Insert into DB."""
        return {
            'gigagroup': entity.gigagroup or False,
            'has_geo': entity.has_geo or False,
            'participants_count': entity.participants_count or 0,
            'title': entity.title or '',
            'access_hash': str(entity.access_hash),
            'fake': entity.fake or False,
            'restricted': entity.restricted or False,
            'scam': entity.scam or False,
            'group_username': entity.username or '',
            'verified': entity.verified or False
        }

    @staticmethod
    def __map_chat(entity: Chat) -> Dict:
        """Map Telethon Chat to TEx Dict to Insert into DB."""
        return {
            'gigagroup': False,
            'has_geo': False,
            'participants_count': entity.participants_count or 0,
            'title': entity.title or '',
            'access_hash': '',
            'fake': False,
            'restricted': False,
            'scam': False,
            'group_username': '',
            'verified': False
        }

    @staticmethod
    def __map_user(entity: User) -> Dict:
        """Map Telethon User to TEx Dict to Insert into DB."""
        return {
            'gigagroup': False,
            'has_geo': False,
            'participants_count': 0,
            'title': entity.username or (entity.phone or ''),
            'access_hash': str(entity.access_hash),
            'fake': entity.fake or False,
            'restricted': entity.restricted or False,
            'scam': entity.scam or False,
            'group_username': entity.username or '',
            'verified': entity.verified or False
        }
