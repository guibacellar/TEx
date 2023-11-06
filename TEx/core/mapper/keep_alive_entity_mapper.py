"""Signal Entity Mapper."""
from __future__ import annotations

from configparser import SectionProxy
from typing import Optional

from TEx.models.facade.signal_entity_model import SignalEntity


class SignalEntityMapper:
    """Signal Entity Mapper."""

    @staticmethod
    def to_entity(section_proxy: Optional[SectionProxy]) -> SignalEntity:
        """Map the Configuration KEEP_ALIVE to Entity."""
        # Build Model
        if section_proxy:
            return SignalEntity(
                enabled=section_proxy.get('enabled', fallback='false') == 'true',
                keep_alive_interval=int(section_proxy.get('keep_alive_interval', fallback='0')),
                notifiers={
                    'KEEP-ALIVE': section_proxy.get('keep_alive_notifer', fallback='').split(','),
                    'INITIALIZATION': section_proxy.get('initialization_notifer', fallback='').split(','),
                    'SHUTDOWN': section_proxy.get('shutdown_notifer', fallback='').split(','),
                    'NEW-GROUP': section_proxy.get('new_group_notifer', fallback='').split(','),
                },
            )

        return SignalEntity(
            enabled=False,
            keep_alive_interval=300,
            notifiers={
                'KEEP-ALIVE': [],
                'INITIALIZATION': [],
                'SHUTDOWN': [],
                'NEW-GROUP': [],
            },
        )
