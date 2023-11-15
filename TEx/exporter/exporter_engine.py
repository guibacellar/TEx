"""Exporter Engine."""
from __future__ import annotations

import logging
from configparser import ConfigParser
from typing import Dict, List, Union

from TEx.exporter.pandas_rolling_exporter import PandasRollingExporter
from TEx.exporter.exporter_base import BaseExporter
from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.models.facade.signal_notification_model import SignalNotificationEntityModel

logger = logging.getLogger('TelegramExplorer')


class ExporterEngine:
    """Primary Export Engine."""

    def __init__(self) -> None:
        """Initialize Exporter Engine."""
        self.exporters: Dict = {}

    def __load_exporters(self, config: ConfigParser) -> None:
        """Load all Registered Exporters."""
        registered_exporters: List[str] = [item for item in config.sections() if 'EXPORTER.' in item]

        for register in registered_exporters:
            if 'ROLLING_PANDAS' in register:

                exporter: PandasRollingExporter = PandasRollingExporter()
                exporter.configure(config=config[register])

                self.exporters.update({
                    register: {'instance': exporter},
                    })

    def configure(self, config: ConfigParser) -> None:
        """Configure Finder."""
        self.__load_exporters(config)

    async def run(self, exporters: List[str], entity: FinderNotificationMessageEntity, rule_id: str, source: str) -> None:
        """Dispatch all Exporting Processes."""
        if len(exporters) == 0:
            return

        for dispatcher_name in exporters:

            target_exporter: BaseExporter = self.exporters[dispatcher_name]['instance']

            try:
                await target_exporter.run(entity=entity, rule_id=rule_id, source=source)

            except Exception:  # Yes, Catch All
                logging.exception('Unable to Export Data')
