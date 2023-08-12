"""Telegram Checker Handler."""
import logging
import os.path
from configparser import ConfigParser
from typing import Dict

from telethon import TelegramClient

from TEx.core.base_module import BaseModule

logger = logging.getLogger()


class TelegramConnector(BaseModule):
    """Telegram Connection Manager - Connect."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        # Check if Need a Connection
        need_connection: bool = args['connect'] or args['load_groups'] or args['download_messages'] or args['sent_report_telegram'] or args['listen']
        if not need_connection:
            return

        # Check Activation Command
        if args['connect']:  # New Connection
            logger.info('\t\tAuthorizing on Telegram...')

            # Connect
            client = TelegramClient(
                os.path.join(config['CONFIGURATION']['data_path'], 'session', config['CONFIGURATION']['phone_number']),
                config['CONFIGURATION']['api_id'],
                config['CONFIGURATION']['api_hash'],
                catch_up=True,
                device_model='TeX'
                )
            await client.start(phone=config['CONFIGURATION']['phone_number'])
            client.session.save()

            # Save Data into State File
            data['telegram_connection'] = {
                'api_id': config['CONFIGURATION']['api_id'],
                'api_hash': config['CONFIGURATION']['api_hash'],
                'target_phone_number': config['CONFIGURATION']['phone_number']
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
                os.path.join(config['CONFIGURATION']['data_path'], 'session', config['CONFIGURATION']['phone_number']),
                data['telegram_connection']['api_id'],
                data['telegram_connection']['api_hash'],
                catch_up=True,
                device_model='TeX'
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
