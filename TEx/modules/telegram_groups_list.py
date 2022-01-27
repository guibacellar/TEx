"""Telegram Group List."""

import base64
import json
import logging
import os
import pathlib
from configparser import ConfigParser
from time import sleep
from typing import Dict, List, Optional, Tuple

import telethon.tl.types
from telethon import TelegramClient
from telethon.errors import ChatAdminRequiredError
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import ChatPhoto, InputPeerEmpty, Message, MessageService, PeerUser
from telethon.tl.types.messages import Dialogs

from TEx.core.base_module import BaseModule
from TEx.core.temp_file import TempFileHandler
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMessageDatabaseManager, \
    TelegramUserDatabaseManager
from TEx.models.database.telegram_db_model import TelegramGroupOrmEntity

logger = logging.getLogger()


class TelegramGroupList(BaseModule):
    """List all Groups on Telegram Account."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not args['list_groups']:
            logger.info('\t\tModule is Not Enabled...')
            return

        # Check Data Dict
        if 'groups' not in data:
            data['groups'] = {}

        if 'members' not in data:
            data['members'] = {}

        # Get all Groups from DB
        db_groups: List[TelegramGroupOrmEntity] = TelegramGroupDatabaseManager.get_all_by_phone_number(
            args['target_phone_number'])
        logger.info(f'\t\tFound {len(db_groups)} Groups')

        # Get the Bigger Username Size
        max_username_size: int = max(
            [len(item.group_username) if item.group_username is not None else 0 for item in db_groups]
            )

        # Get the Bigger Title Size
        max_title_size: int = max(
            [len(item.title) if item.title is not None else 0 for item in db_groups]
        )

        # Print Groups
        logger.info(f'\t\tID       \t{"Username".ljust(max_username_size)}\t{"Title".ljust(max_title_size)}')
        for group in db_groups:
            formatted_username: str = group.group_username.ljust(max_username_size) if group.group_username is not None else 'UNDEFINED'.ljust(max_username_size)
            formatted_title: str = group.title.ljust(max_title_size) if group.title is not None else 'UNDEFINED'.ljust(max_title_size)
            logger.info(f'\t\t{group.id}\t{formatted_username}\t{formatted_title}')
