"""Base Class for All Notifiers."""
from __future__ import annotations

import abc
import hashlib
from configparser import SectionProxy
from typing import Optional, Tuple, Union

from cachetools import TTLCache

from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.models.facade.signal_notification_model import SignalNotificationEntityModel


class BaseNotifier:
    """Base Notifier."""

    def __init__(self) -> None:
        """Initialize the Base Notifier."""
        self.cache: Optional[TTLCache] = None
        self.timeout_seconds: int
        self.media_attachments_enabled: bool
        self.media_attachments_max_size_bytes: int

    def configure_base(self, config: SectionProxy) -> None:
        """Configure Base Notifier."""
        self.cache = TTLCache(maxsize=4096, ttl=int(config.get('prevent_duplication_for_minutes', fallback='240')) * 60)
        self.timeout_seconds = int(config.get('timeout_seconds', fallback='30'))
        self.media_attachments_enabled = config.get('media_attachments_enabled', fallback='false') == 'true'
        self.media_attachments_max_size_bytes = int(config.get('media_attachments_max_size_bytes', fallback='10000000'))

    def check_is_duplicated(self, message: str) -> Tuple[bool, str]:
        """Check if Message is Duplicated on Notifier."""
        if not message or self.cache is None:
            return False, ''

        # Compute Deduplication Tag
        tag: str = hashlib.md5(message.encode('UTF-8')).hexdigest()

        # If Found, Return True
        if self.cache.get(tag):
            return True, tag

        # Otherwise, Just Insert and Return False
        self.cache[tag] = True
        return False, tag

    @abc.abstractmethod
    async def run(self, entity: Union[FinderNotificationMessageEntity, SignalNotificationEntityModel], rule_id: str, source: str) -> None:
        """Run the Notification Process."""
