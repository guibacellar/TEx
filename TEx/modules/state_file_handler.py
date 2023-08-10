"""State File Handler."""

import json
import logging
from configparser import ConfigParser
from typing import Dict

from TEx.core.base_module import BaseModule
from TEx.core.state_file import StateFileHandler

logger = logging.getLogger()


class LoadStateFileHandler(BaseModule):
    """Module that Loads Previous Created State File."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        state_file_name: str = config['MODULE_LoadStateFileHandler']['file_name'].replace("{0}", config['CONFIGURATION']['phone_number'])

        if StateFileHandler.file_exist(state_file_name):
            data.update(
                json.loads(StateFileHandler.read_file_text(state_file_name))
                )
            logger.debug("\t\tState File Loaded.")


class SaveStateFileHandler(BaseModule):
    """Module that Save a New State File."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        state_file_name: str = config['MODULE_SaveStateFileHandler']['file_name'].replace("{0}", config['CONFIGURATION']['phone_number'])

        StateFileHandler.write_file_text(
            state_file_name,
            json.dumps(data)
            )
