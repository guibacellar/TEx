"""Database Handler."""

import logging
import os
from configparser import ConfigParser
from typing import Dict

from TEx.core.base_module import BaseModule
from TEx.core.dir_manager import DirectoryManagerUtils

logger = logging.getLogger()


class DataStructureHandler(BaseModule):
    """Handle the Basic Directory Structure."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute."""
        if 'data_path' not in args:
            return

        DirectoryManagerUtils.ensure_dir_struct(os.path.join(args["data_path"], 'export'))
        DirectoryManagerUtils.ensure_dir_struct(os.path.join(args["data_path"], 'download'))
        DirectoryManagerUtils.ensure_dir_struct(os.path.join(args["data_path"], 'profile_pic'))
        DirectoryManagerUtils.ensure_dir_struct(os.path.join(args["data_path"], 'media'))
        DirectoryManagerUtils.ensure_dir_struct(os.path.join(args["data_path"], 'session'))
