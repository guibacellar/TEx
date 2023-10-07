"""Database Handler."""
from __future__ import annotations

import logging
import os
from configparser import ConfigParser
from typing import Dict

from TEx.core.base_module import BaseModule
from TEx.core.dir_manager import DirectoryManagerUtils

logger = logging.getLogger('TelegramExplorer')


class DataStructureHandler(BaseModule):
    """Handle the Basic Directory Structure."""

    async def can_activate(self, config: ConfigParser, args: Dict, data: Dict) -> bool:
        """
        Abstract Method for Module Activation Function.

        :return:
        """
        return 'data_path' in args

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute."""
        if not await self.can_activate(config, args, data):
            return

        DirectoryManagerUtils.ensure_dir_struct(os.path.join(args['data_path'], 'export'))
        DirectoryManagerUtils.ensure_dir_struct(os.path.join(args['data_path'], 'download'))
        DirectoryManagerUtils.ensure_dir_struct(os.path.join(args['data_path'], 'profile_pic'))
        DirectoryManagerUtils.ensure_dir_struct(os.path.join(args['data_path'], 'media'))
        DirectoryManagerUtils.ensure_dir_struct(os.path.join(args['data_path'], 'session'))
