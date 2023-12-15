"""Base Class for All Exporters."""
from __future__ import annotations

import abc
import logging
import os
from configparser import SectionProxy
from pathlib import Path
from typing import List

from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity

logger = logging.getLogger('TelegramExplorer')


class BaseExporter:
    """Base Notifier."""

    def __init__(self) -> None:
        """Initialize the Base Exporter."""
        self.file_root_path: str = ''

    def configure_base(self, config: SectionProxy) -> None:
        """Configure Base Exporter."""
        self.file_root_path = config.get('file_root_path')

    @abc.abstractmethod
    async def run(self, entity: FinderNotificationMessageEntity, rule_id: str) -> None:
        """Run the Exporting Process."""

    @abc.abstractmethod
    def shutdown(self) -> None:
        """Shutdown and Flush all Data into Disk."""

    def _keep_last_files_only(self, directory_path: str, file_count: int) -> None:
        """Ensure the Directory Contains Only the 'file_count' newest files. Note: CHAT GPT-4 Assisted Code."""
        if not os.path.exists(directory_path):
            return

        # List All Files
        files: List = [
            os.path.join(directory_path, file) for file in os.listdir(directory_path) if
            Path(os.path.join(directory_path, file)).is_file()
            ]

        # Check File Limit
        if len(files) <= file_count:
            return

        # Sort Files by Date/Time
        files.sort(key=lambda x: Path(x).stat().st_mtime)

        # Compute File Remove Counter
        files_to_delete: int = len(files) - file_count

        # Remove Old Files
        for i in range(files_to_delete):
            try:
                os.remove(files[i])
            except Exception as ex:
                logger.exception(msg=f'Unable to Remove {files[i]}', exc_info=ex)
