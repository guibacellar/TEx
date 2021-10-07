"""Telegram Group Printer."""
import logging
from configparser import ConfigParser
from typing import Dict

from TEx.core.base_module import BaseModule

logger = logging.getLogger()


class TelegramGroupPrinter(BaseModule):
    """Print the Name of all Groups."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        # Check Data Dict
        if 'groups' not in data:
            return

        # Print Group Names
        for _key, value in data['groups'].items():
            logger.info(f'\t\tGroup: {value["username"]} (ID: {value["id"]})')
