"""Base Class for All Exporters."""
from __future__ import annotations

import abc
import hashlib
from configparser import SectionProxy
from typing import Optional, Tuple, Union

from cachetools import TTLCache

from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.models.facade.signal_notification_model import SignalNotificationEntityModel


class BaseExporter:
    """Base Notifier."""

    def __init__(self) -> None:
        """Initialize the Base Exporter."""
        self.file_root_path: str = ''

    def configure_base(self, config: SectionProxy) -> None:
        """Configure Base Exporter."""
        self.file_root_path = config.get('file_root_path')

    @abc.abstractmethod
    async def run(self, entity: Union[FinderNotificationMessageEntity, SignalNotificationEntityModel], rule_id: str, source: str) -> None:
        """Run the Exporting Process."""
