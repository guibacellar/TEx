"""Base Class for All Notifiers."""
import abc
import hashlib
from configparser import SectionProxy
from typing import Optional, Tuple

from cachetools import TTLCache
from telethon.events import NewMessage


class BaseNotifier:
    """Base Notifier."""

    def __init__(self) -> None:
        """Initialize the Base Notifier."""
        self.cache: Optional[TTLCache] = None

    def configure_base(self, config: SectionProxy) -> None:
        """Configure Base Notifier."""
        self.cache = TTLCache(maxsize=4096, ttl=int(config['prevent_duplication_for_minutes']) * 60)

    def check_is_duplicated(self, message: str) -> Tuple[bool, str]:
        """Check if Message is Duplicated on Notifier."""
        if not message or self.cache is None:
            return False, ''

        # Compute Deduplication Tag
        tag: str = hashlib.md5(message.encode('UTF-8')).hexdigest()  # nosec

        # If Found, Return True
        if self.cache.get(tag):
            return True, tag

        # Otherwise, Just Insert and Return False
        self.cache[tag] = True
        return False, tag

    @abc.abstractmethod
    async def run(self, message: NewMessage.Event, rule_id: str) -> None:
        """Run the Notification Process."""
