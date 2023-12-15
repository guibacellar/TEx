"""Telegram Checker Handler."""
from __future__ import annotations

import logging
import os.path
import platform
from configparser import ConfigParser, SectionProxy
from typing import Dict, Optional, cast

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

        # Check Activation Command
        if args['connect']:  # New Connection
            logger.info('\t\tAuthorizing on Telegram...')

            # Connect
            client = await self.__get_telegram_client(
                session_dir=session_dir,
                config=config,
                api_id=config['CONFIGURATION']['api_id'],
                api_hash=config['CONFIGURATION']['api_hash'],
            )
            await client.start(phone=config['CONFIGURATION']['phone_number'])
            client.session.save()

            # Save Data into State File
            data['telegram_connection'] = {
                'api_id': config['CONFIGURATION']['api_id'],
                'api_hash': config['CONFIGURATION']['api_hash'],
                'target_phone_number': config['CONFIGURATION']['phone_number'],
                }

        else:  # Reuse Previous Connection
            # Check if Contains the Required Data
            if 'telegram_connection' not in data or \
                    'api_id' not in data['telegram_connection'] or \
                    'api_hash' not in data['telegram_connection'] or \
                    'target_phone_number' not in data['telegram_connection']:
                logger.warning('\t\tNot Authenticated on Telegram. Please use the "connect" command.')
                data['internals']['panic'] = True
                return

            client = await self.__get_telegram_client(
                session_dir=session_dir,
                config=config,
                api_id=data['telegram_connection']['api_id'],
                api_hash=data['telegram_connection']['api_hash'],
            )
            await client.start(phone=data['telegram_connection']['target_phone_number'])

        data['telegram_client'] = client
        logger.info(f'\t\tUser Authorized on Telegram: {await client.is_user_authorized()}')

    async def __get_telegram_client(self, session_dir: str, config: ConfigParser, api_id: str, api_hash: str) -> TelegramClient:
        """Return a Telegram Client."""
        device_model: str = self.__get_device_model_name(config=config)

        proxy_settings: Optional[Dict] = await self.__get_proxy_settings(config=config)
        if proxy_settings:
            logger.info(f'\t\tUsing {proxy_settings["proxy_type"]} Proxy')

        return TelegramClient(
            os.path.join(session_dir, config['CONFIGURATION']['phone_number']),
            api_id, api_hash,
            catch_up=True,
            device_model=device_model,
            proxy=proxy_settings,
            timeout=int(config['CONFIGURATION'].get('timeout', fallback='10')),
        )

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

            except Exception:
                return 'TeX'

        return device_model_name

    async def __get_proxy_settings(self, config: ConfigParser) -> Optional[Dict]:
        """Return Proxy Setting."""
        # Check if Config Contains Proxy
        if not config.has_section('PROXY'):
            return None

        proxy_section: SectionProxy = config['PROXY']

        # Check Minimum Proxy Settings
        if 'type' not in proxy_section or 'address' not in proxy_section or 'port' not in proxy_section:
            return None

        # Set Basic Result
        h_result: Dict = {
            'proxy_type': proxy_section['type'],
            'addr': proxy_section['address'],
            'port': int(proxy_section['port']),
        }

        # Check Proxy Auth and Password
        if 'username' in proxy_section and proxy_section['username'] != '':
            h_result['username'] = proxy_section['username']

        if 'password' in proxy_section and proxy_section['password'] != '':
            h_result['password'] = proxy_section['password']

        if 'rdns' in proxy_section and proxy_section['rdns'] != '':
            h_result['rdns'] = bool(proxy_section['rdns'])

        return h_result


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
