"""Exporter Engine."""
from __future__ import annotations

import logging
from configparser import ConfigParser
from typing import Dict, List

from TEx.exporter.exporter_base import BaseExporter
from TEx.exporter.pandas_rolling_exporter import PandasRollingExporter
from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity

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
                exporter.configure(config=config[register], source=config['CONFIGURATION']['phone_number'])

                self.exporters.update({
                    register: {'instance': exporter},
                    })

    def configure(self, config: ConfigParser) -> None:
        """Configure Finder."""
        self.__load_exporters(config)

    async def run(self, exporters: List[str], entity: FinderNotificationMessageEntity, rule_id: str) -> None:
        """Dispatch all Exporting Processes."""
        if len(exporters) == 0:
            return

        for dispatcher_name in exporters:

            target_exporter: BaseExporter = self.exporters[dispatcher_name]['instance']

            try:
                await target_exporter.run(entity=entity, rule_id=rule_id)

            except Exception as _ex:  # Yes, Catch All
                logging.exception('Unable to Export Data')

    async def shutdown(self) -> None:
        """Shutdown all Exporters and Flush all to Disk."""
        for dispatcher_name in self.exporters:

            target_exporter: BaseExporter = self.exporters[dispatcher_name]['instance']

            try:
                target_exporter.shutdown()

            except Exception as _ex:  # Yes, Catch All
                logging.exception(f'Unable to Shutdown the "{dispatcher_name}" Exporter Gracefully. Data may be lost.')
