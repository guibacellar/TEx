"""Signals Notification Engine."""
from __future__ import annotations

from configparser import ConfigParser
from datetime import datetime
from typing import List

import pytz

from TEx.core.mapper.keep_alive_entity_mapper import SignalEntityMapper
from TEx.models.facade.signal_entity_model import SignalEntity
from TEx.models.facade.signal_notification_model import SignalNotificationEntityModel
from TEx.notifier.notifier_engine import NotifierEngine


class SignalsEngineFactory:
    """Signals Notification Engine Factory."""

    @staticmethod
    def get_instance(config: ConfigParser, notification_engine: NotifierEngine, source: str) -> SignalsEngine:
        """Get the Signals Engine Instance."""
        return SignalsEngine(
            entity=SignalEntityMapper.to_entity(section_proxy=config['SIGNALS'] if config.has_section('SIGNALS') else None),
            notification_engine=notification_engine,
            source=source,
        )


class SignalsEngine:
    """Signals Notification Engine."""

    def __init__(self, entity: SignalEntity, notification_engine: NotifierEngine, source: str) -> None:
        """Initialize the Signals Engine."""
        self.signal_entity: SignalEntity = entity
        self.messages_sent: int = 0
        self.notification_engine: NotifierEngine = notification_engine
        self.source: str = source

    @property
    def keep_alive_interval(self) -> int:
        """Return the Keep Alive Engine Interval."""
        return self.signal_entity.keep_alive_interval

    def inc_messages_sent(self) -> None:
        """Increment the Messages Sent Counter."""
        self.messages_sent += 1

    async def keep_alive(self) -> None:
        """Send the Keep Alive."""
        await self.__send_signal(
            entity=SignalNotificationEntityModel(
                date_time=datetime.now(tz=pytz.UTC),
                content=f'Messages Processed in Period: {self.messages_sent}',
                signal='KEEP-ALIVE',
            ),
        )

        # Reset Messages Sent Counter
        self.messages_sent = 0

    async def shutdown(self) -> None:
        """Send the Shutdown."""
        await self.__send_signal(
            entity=SignalNotificationEntityModel(
                date_time=datetime.now(tz=pytz.UTC),
                content=f'Last Messages Processed in Period: {self.messages_sent}',
                signal='SHUTDOWN',
            ),
        )

    async def init(self) -> None:
        """Send the Shutdown."""
        await self.__send_signal(
            entity=SignalNotificationEntityModel(
                date_time=datetime.now(tz=pytz.UTC),
                content='',
                signal='INITIALIZATION',
            ),
        )

    async def new_group(self, group_id: str, group_title: str) -> None:
        """Send the New Group Event."""
        await self.__send_signal(
            entity=SignalNotificationEntityModel(
                date_time=datetime.now(tz=pytz.UTC),
                content=f'ID: {group_id} | Title: "{group_title}"',
                signal='NEW-GROUP',
            ),
        )

    async def __send_signal(self, entity: SignalNotificationEntityModel) -> None:
        """Send the Signal."""
        signal_notifiers: List[str] = self.signal_entity.notifiers[entity.signal]

        if len(signal_notifiers) == 0:
            return

        await self.notification_engine.run(
            notifiers=signal_notifiers,
            entity=entity,
            rule_id='SIGNALS',
            source=self.source,
        )
