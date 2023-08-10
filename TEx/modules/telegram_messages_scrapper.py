"""Telegram Group Scrapper."""
import logging
from configparser import ConfigParser
from time import sleep
from typing import Dict, List, Optional

import pytz
import telethon.errors.rpcerrorlist
from telethon import TelegramClient
from telethon.tl.types import (Message, MessageService, PeerChannel, PeerUser)

from TEx.core.base_module import BaseModule
from TEx.core.media_handler import UniversalTelegramMediaHandler
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMessageDatabaseManager
from TEx.models.database.telegram_db_model import TelegramGroupOrmEntity

logger = logging.getLogger()


class TelegramGroupMessageScrapper(BaseModule):
    """Download all Messages from Telegram Groups."""

    def __init__(self) -> None:
        """Class Initializer."""
        self.media_handler: UniversalTelegramMediaHandler = UniversalTelegramMediaHandler()

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not args['download_messages']:
            logger.info('\t\tModule is Not Enabled...')
            return

        # Get Client
        client: TelegramClient = data['telegram_client']

        # Load Groups from DB
        groups: List[TelegramGroupOrmEntity] = TelegramGroupDatabaseManager.get_all_by_phone_number(
            config['CONFIGURATION']['phone_number'])
        logger.info(f'\t\tFound {len(groups)} Groups')

        # Filter Groups
        if args['group_id'] and args['group_id'] != '*':
            group_ids: List[int] = [int(group_id) for group_id in args['group_id'].split(',')]
            groups = [group for group in groups if group.id in group_ids]

            logger.info(f'\t\tApplied Groups Filtering... {len(groups)} remaining')

        for group in groups:
            try:
                await self.__download_messages(
                    group_id=group.id,
                    client=client,
                    group_name=group.title,
                    download_media=not args['ignore_media'],
                    data_path=config['CONFIGURATION']['data_path'],
                    iter_message_type=PeerChannel
                    )
            except ValueError as ex:
                logger.info('\t\t\tUnable to Download Messages...')
                logger.error(ex)
            except telethon.errors.rpcerrorlist.ChannelPrivateError as ex:
                logger.info('\t\t\tUnable to Download dua a Channel Private Error Restriction...')
                logger.error(ex)

    async def __download_messages(self, group_id: int, group_name: str, client: TelegramClient, download_media: bool, data_path: str, iter_message_type: type) -> None:  # pylint: disable=R0913
        """Download all Messages from a Single Group."""
        # Main Download Loop
        while True:

            # Loop Control
            records: int = 0

            # Get the Latest OffSet from Group
            last_offset: Optional[int] = TelegramMessageDatabaseManager.get_max_id_from_group(group_id=group_id)

            # Log
            logger.info(f'\t\tDownload Messages from "{group_name}" > Last Offset: {last_offset}')

            # Wait to Prevent Telegram Flood Detection
            sleep(1)

            # Get all Chats from a Single Group
            # https://docs.telethon.dev/en/latest/modules/client.html#telethon.client.messages.MessageMethods.iter_messages
            async for message in client.iter_messages(
                    iter_message_type(group_id),
                    reverse=True,
                    limit=500,
                    min_id=last_offset if last_offset is not None else -1
                    ):

                # Ignore MessageService Messages
                if isinstance(message, MessageService):
                    continue

                # Loop Control
                records += 1

                # Handle Unknown Types
                if not isinstance(message, Message):
                    logger.debug(f'\t\t{type(message)}')

                if message.reply_to is not None:
                    pass

                if message.reply_to_msg_id:
                    pass

                values: Dict = {
                    'id': message.id,
                    'group_id': group_id,
                    'date_time': message.date.astimezone(tz=pytz.utc),
                    'message': message.message,
                    'raw': message.raw_text,
                    'to_id': message.to_id.channel_id if message.to_id is not None else None,
                    'media_id': await self.media_handler.handle_medias(message, group_id, data_path) if download_media else None
                    }

                if message.from_id is not None:
                    if isinstance(message.from_id, PeerUser):
                        values['from_id'] = message.from_id.user_id
                        values['from_type'] = 'User'
                    else:
                        pass

                # Add to DB
                TelegramMessageDatabaseManager.insert(values)

            # Exit Rule
            if records == 0:
                break
