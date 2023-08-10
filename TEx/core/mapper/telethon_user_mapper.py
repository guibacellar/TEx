"""Telethon User Entity Mapper."""
from typing import Dict

from telethon.tl.types import User


class TelethonUserEntiyMapper:
    """Telethon User Entity Mapper."""

    @staticmethod
    def to_database_dict(member: User) -> Dict:
        """Map Telethon User to TeX Dict to Insert on DB."""
        # Build Model
        value: Dict = {
            'id': member.id,
            'is_bot': member.bot,
            'is_fake': member.fake,
            'is_self': member.is_self,
            'is_scam': member.scam,
            'is_verified': member.verified,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'username': member.username,
            'phone_number': member.phone,
            'photo_id': None,  # Reserved for Future Version
            'photo_base64': None,  # Reserved for Future Version
            'photo_name': None  # Reserved for Future Version
            }

        return value
