"""Database Handler."""

import argparse
import logging
from configparser import ConfigParser
from typing import Dict

from TEx.core.base_module import BaseModule
from TEx.database.db_initializer import DbInitializer
from TEx.core.temp_file import TempFileHandler

logger = logging.getLogger()


class DatabaseHanbler(BaseModule):
    """Module That Handle the Internal DB."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:

        # Initialize DB
        DbInitializer.init(args['data_path'], args)

        # Expire Temp Files
        TempFileHandler.remove_expired_entries()

