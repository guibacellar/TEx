"""Telegram Group Listener."""
import logging
from configparser import ConfigParser
from typing import Dict, List

import pytz
from telethon import TelegramClient, events
from telethon.events import NewMessage
from telethon.tl.types import (Channel, Message, PeerUser, User)

from TEx.core.base_module import BaseModule
from TEx.core.mapper.telethon_channel_mapper import TelethonChannelEntiyMapper
from TEx.core.mapper.telethon_user_mapper import TelethonUserEntiyMapper
from TEx.core.media_handler import UniversalTelegramMediaHandler
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMessageDatabaseManager, \
    TelegramUserDatabaseManager

logger = logging.getLogger()


class TelegramGroupMessageListener(BaseModule):
    """Download all Messages from Telegram Groups."""

    def __init__(self) -> None:
        """Initialize Listener Module."""
        self.download_media: bool = False
        self.data_path: str = ''
        self.group_ids: List[int] = []
        self.media_handler: UniversalTelegramMediaHandler = UniversalTelegramMediaHandler()
        self.target_phone_number: str = ''

    async def __handler(self, event: NewMessage.Event) -> None:
        """Handle the Message."""
        # Get Message
        message: Message = event.message

        # Apply Filter (If group filtering are enabled)
        if len(self.group_ids) > 0 and event.chat.id not in self.group_ids:
            logger.debug(f'\t\tMessage Filtered (GroupID={event.chat.id}) ...')
            return

        if event and not event.chat:
            return  # TO_DO: Need to Be Handled in Future Version

        # Ensure Group Exists on DB
        await self.__ensure_group_exists(event=event)

        # Create Dict with All Value
        values: Dict = {
            'id': message.id,
            'group_id': event.chat.id,
            'date_time': message.date.astimezone(tz=pytz.utc),
            'message': message.message,
            'raw': message.raw_text,
            'to_id': message.to_id.channel_id if message.to_id is not None else None,
            'media_id': await self.media_handler.handle_medias(message, event.chat.id,
                                                               self.data_path) if self.download_media else None,
            'is_reply': message.is_reply,
            'reply_to_msg_id': message.reply_to.reply_to_msg_id if message.is_reply else None
            }

        # Process Sender ID
        if message.from_id is not None:
            if isinstance(message.from_id, PeerUser):

                values['from_id'] = message.from_id.user_id
                values['from_type'] = 'User'

                # Ensure User Exists
                await self.__ensure_user_exists(event=event)

            else:
                pass

        # Add to DB
        TelegramMessageDatabaseManager.insert(values)

    async def __ensure_user_exists(self, event: NewMessage.Event) -> None:
        """
        Ensure the User Exists on DB.

        :param event:
        :return:
        """
        # Check if User Already in DB or is New One -- REFACTORY
        if not TelegramUserDatabaseManager.get_by_id(pk=event.from_id.user_id):
            logger.warning(
                f'\t\tUser "{event.from_id.user_id}" was not found on DB. Performing automatic synchronization.')

            # Retrieve User
            result: User = await event.get_sender()

            # Perform Synchronization
            if result:
                user_dict_data: Dict = TelethonUserEntiyMapper.to_database_dict(result)
                TelegramUserDatabaseManager.insert_or_update(user_dict_data)

    async def __ensure_group_exists(self, event: NewMessage.Event) -> None:
        """
        Ensure the Group/Channel Exists on DB.

        :param event:
        :return:
        """
        # Check if Group Already in DB or is New One
        if not TelegramGroupDatabaseManager.get_by_id(pk=event.chat.id):
            logger.warning(
                f'\t\tGroup "{event.chat.id}" not found on DB. Performing automatic synchronization. Consider execute "load_groups" command to perform a full group synchronization (Members and Group Cover Photo).')

            # Retrieve Group Definitions
            result: Channel = await event.get_chat()

            # Perform Synchronization
            if result:
                group_dict_data: Dict = TelethonChannelEntiyMapper.to_database_dict(
                    channel=result,
                    target_phone_numer=self.target_phone_number
                    )

                TelegramGroupDatabaseManager.insert_or_update(group_dict_data)

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not args['listen']:
            logger.info('\t\tModule is Not Enabled...')
            return

        # Update Module Global Info
        self.download_media = not args['ignore_media']
        self.data_path = config['CONFIGURATION']['data_path']
        self.target_phone_number = config['CONFIGURATION']['phone_number']

        # Update Module Group Filtering Info
        if args['group_id'] and args['group_id'] != '*':
            self.group_ids = [int(group_id) for group_id in args['group_id'].split(',')]
            logger.info(f'\t\tApplied Groups Filtering... {len(self.group_ids)} selected')

        # Get Client
        client: TelegramClient = data['telegram_client']

        # Register Handlers
        client.add_event_handler(self.__handler, events.NewMessage)

        # Catch Up Past Messages
        logger.info('\t\tListening Past Messages...')
        await client.catch_up()

        # Read all Messages from Now
        logger.info('\t\tListening New Messages...')
        await client.run_until_disconnected()  # Code Stops Here until telegram disconnects

        logger.info('\t\tTelegram Client Disconnected...')
