"""Execution Configuration Loader."""

import logging
import os.path
from configparser import ConfigParser
from typing import Dict

from TEx.core.base_module import BaseModule

logger = logging.getLogger()


class ExecutionConfigurationHandler(BaseModule):
    """Module That Handle the Input Arguments."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Load Configuration for Execution."""
        logger.info('[*] Loading Execution Configurations:')

        if not os.path.exists(args['config']):
            logger.fatal(f'[?] CONFIGURATION FILE NOT FOUND AT \"{args["config"]}\"')
            data['internals']['panic'] = True
            return

        config.read(args['config'])
