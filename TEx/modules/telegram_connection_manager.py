"""Telegram Checker Handler."""
import logging
from configparser import ConfigParser
from typing import Dict

from telethon import TelegramClient
from telethon.sessions import StringSession
from TEx.core.base_module import BaseModule

logger = logging.getLogger()


class TelegramConnector(BaseModule):
    """Telegram Connection Manager - Connect."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        # Check if Need a Connection
        need_connection: bool = args['connect'] or args['load_groups'] or args['download_messages']
        if not need_connection:
            return

        # Check Activation Command
        if args['connect']:  # New Connection
            logger.info('\t\tAuthorizing on Telegram...')

            # Connect
            client = TelegramClient(
                StringSession(),
                args['api_id'],
                args['api_hash'],
                )
            await client.start(phone=args['target_phone_number'])

            # Save Data into State File
            data['telegram_connection'] = {
                'api_id': args['api_id'],
                'api_hash': args['api_hash'],
                'target_phone_number': args['target_phone_number'],
                'session_code': client.session.save()
                }

        else:  # Reuse Previous Connection

            # Check if Contains the Required Data
            if 'telegram_connection' not in data or \
                    'api_id' not in data['telegram_connection'] or \
                    'api_hash' not in data['telegram_connection'] or \
                    'target_phone_number' not in data['telegram_connection']:
                logger.warning('\t\tNot Authenticated on Telegram. Please use the "connect" command.')
                return

            client = TelegramClient(
                StringSession(data['telegram_connection']['session_code']),
                data['telegram_connection']['api_id'],
                data['telegram_connection']['api_hash'],
                )
            await client.start(phone=data['telegram_connection']['target_phone_number'])

        data['telegram_client'] = client
        logger.info(f'\t\tUser Authorized on Telegram: {await client.is_user_authorized()}')


class TelegramDisconnector(BaseModule):
    """Telegram Connection Manager - Connect."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if 'telegram_client' in data and data['telegram_client']:
            await data['telegram_client'].disconnect()
            del data['telegram_client']
