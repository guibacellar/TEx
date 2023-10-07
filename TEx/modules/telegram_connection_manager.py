"""Telegram Checker Handler."""
import logging
import os.path
import platform
from configparser import ConfigParser
from typing import Dict, cast

from telethon import TelegramClient

from TEx.core.base_module import BaseModule

logger = logging.getLogger('TelegramExplorer')


class TelegramConnector(BaseModule):
    """Telegram Connection Manager - Connect."""

    async def can_activate(self, config: ConfigParser, args: Dict, data: Dict) -> bool:
        """
        Abstract Method for Module Activation Function.

        :return:
        """
        return cast(bool, args['connect'] or args['load_groups'] or args['download_messages'] or args['sent_report_telegram'] or args['listen'])

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not await self.can_activate(config, args, data):
            return

        # Check if Directory Exists
        session_dir: str = os.path.join(config['CONFIGURATION']['data_path'], 'session')
        if not os.path.exists(session_dir):
            os.mkdir(session_dir)

        device_model: str = self.__get_device_model_name(config=config)

        # Check Activation Command
        if args['connect']:  # New Connection
            logger.info('\t\tAuthorizing on Telegram...')

            # Connect
            client = TelegramClient(
                os.path.join(session_dir, config['CONFIGURATION']['phone_number']),
                config['CONFIGURATION']['api_id'],
                config['CONFIGURATION']['api_hash'],
                catch_up=True,
                device_model=device_model
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
                os.path.join(session_dir, config['CONFIGURATION']['phone_number']),
                data['telegram_connection']['api_id'],
                data['telegram_connection']['api_hash'],
                catch_up=True,
                device_model=device_model
                )
            await client.start(phone=data['telegram_connection']['target_phone_number'])

        data['telegram_client'] = client
        logger.info(f'\t\tUser Authorized on Telegram: {await client.is_user_authorized()}')

    def __get_device_model_name(self, config: ConfigParser) -> str:
        """
        Compute Device Model Name for Telegram API.

        :return:
        """
        # Get Value from Configuration File
        device_model_name: str = config['CONFIGURATION']['device_model'] if 'device_model' in config['CONFIGURATION'] else 'TeX'

        # Check for Automatic Configuration
        if device_model_name == 'AUTO':
            try:
                return platform.uname().machine

            except Exception:  # noqa: B902
                return 'TeX'

        return device_model_name


class TelegramDisconnector(BaseModule):
    """Telegram Connection Manager - Connect."""

    async def can_activate(self, config: ConfigParser, args: Dict, data: Dict) -> bool:
        """
        Abstract Method for Module Activation Function.

        :return:
        """
        return 'telegram_client' in data and data['telegram_client']

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not await self.can_activate(config, args, data):
            return

        await data['telegram_client'].disconnect()
        del data['telegram_client']
