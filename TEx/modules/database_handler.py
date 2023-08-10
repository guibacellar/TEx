"""Database Handler."""

import logging
from configparser import ConfigParser
from typing import Dict

from TEx.core.base_module import BaseModule
from TEx.core.temp_file import TempFileHandler
from TEx.database.db_initializer import DbInitializer

logger = logging.getLogger()


class DatabaseHandler(BaseModule):
    """Module That Handle the Internal DB."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute."""
        # Initialize DB
        DbInitializer.init(config['CONFIGURATION']['data_path'])

        # Expire Temp Files
        TempFileHandler.remove_expired_entries()
