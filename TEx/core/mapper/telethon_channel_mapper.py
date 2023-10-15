"""Telethon Channel Entity Mapper."""
from __future__ import annotations

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
            'source': target_phone_numer,
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
            'gigagroup': entity.gigagroup if entity.gigagroup else False,
            'has_geo': entity.has_geo if entity.has_geo else False,
            'participants_count': entity.participants_count if entity.participants_count else 0,
            'title': entity.title if entity.title else '',
            'access_hash': str(entity.access_hash),
            'fake': entity.fake if entity.fake else False,
            'restricted': entity.restricted if entity.restricted else False,
            'scam': entity.scam if entity.scam else False,
            'group_username': entity.username if entity.username else '',
            'verified': entity.verified if entity.verified else False,
            }

    @staticmethod
    def __map_chat(entity: Chat) -> Dict:
        """Map Telethon Chat to TEx Dict to Insert into DB."""
        return {
            'gigagroup': False,
            'has_geo': False,
            'participants_count': entity.participants_count if entity.participants_count else 0,
            'title': entity.title if entity.title else '',
            'access_hash': '',
            'fake': False,
            'restricted': False,
            'scam': False,
            'group_username': '',
            'verified': False,
            }

    @staticmethod
    def __map_user(entity: User) -> Dict:
        """Map Telethon User to TEx Dict to Insert into DB."""
        return {
            'gigagroup': False,
            'has_geo': False,
            'participants_count': 0,
            'title': entity.username if entity.username else (entity.phone if entity.phone else ''),
            'access_hash': str(entity.access_hash),
            'fake': entity.fake if entity.fake else False,
            'restricted': entity.restricted if entity.restricted else False,
            'scam': entity.scam if entity.scam else False,
            'group_username': entity.username if entity.username else '',
            'verified': entity.verified if entity.verified else False,
            }
