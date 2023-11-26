"""Telegram Group Listener."""
from __future__ import annotations

import asyncio
import contextlib
import logging
import signal
from configparser import ConfigParser
from typing import Dict, List, Optional, Tuple, cast

import pytz
from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import ChannelPrivateError
from telethon.events import NewMessage
from telethon.tl.patched import Message
from telethon.tl.types import Channel, PeerUser, User

from TEx.core.base_module import BaseModule
from TEx.core.mapper.telethon_channel_mapper import TelethonChannelEntityMapper
from TEx.core.mapper.telethon_message_mapper import TelethonMessageEntityMapper
from TEx.core.mapper.telethon_user_mapper import TelethonUserEntiyMapper
from TEx.core.media_handler import UniversalTelegramMediaHandler
from TEx.core.ocr.ocr_engine_base import OcrEngineBase
from TEx.core.ocr.ocr_engine_factory import OcrEngineFactory
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMessageDatabaseManager, TelegramUserDatabaseManager
from TEx.exporter.exporter_engine import ExporterEngine
from TEx.finder.finder_engine import FinderEngine
from TEx.models.facade.media_handler_facade_entity import MediaHandlingEntity
from TEx.notifier.notifier_engine import NotifierEngine
from TEx.notifier.signals_engine import SignalsEngine, SignalsEngineFactory

logger = logging.getLogger('TelegramExplorer')


class TelegramGroupMessageListener(BaseModule):
    """Download all Messages from Telegram Groups."""

    async def can_activate(self, config: ConfigParser, args: Dict, data: Dict) -> bool:
        """
        Abstract Method for Module Activation Function.

        :return:
        """
        return cast(bool, args['listen'])

    def __init__(self) -> None:
        """Initialize Listener Module."""
        self.download_media: bool = False
        self.data_path: str = ''
        self.group_ids: List[int] = []
        self.media_handler: UniversalTelegramMediaHandler = UniversalTelegramMediaHandler()
        self.target_phone_number: str = ''
        self.finder: FinderEngine = FinderEngine()
        self.notification_engine: NotifierEngine = NotifierEngine()
        self.exporter_engine: ExporterEngine = ExporterEngine()
        self.ocr_engine: OcrEngineBase
        self.signals_engine: SignalsEngine
        self.term_signal: bool = False
        self.sleep_task: asyncio.Task

    def __handle_term_signal(self, *args: Tuple) -> None:
        """Handle the Interruption and Termination Signals."""
        self.term_signal = True

        # If Have an Active Sleep, Cancel
        if self.sleep_task:
            self.sleep_task.cancel()

        logger.warning('\t\tTermination Signal Received, please wait to Stop Processing Gracefully.')

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

        # Download Media
        downloaded_media: Optional[MediaHandlingEntity] = await self.media_handler.handle_medias(
            message, event.chat.id, self.data_path,
            ) if self.download_media else None

        # Process OCR
        ocr_content: Optional[str] = None
        if downloaded_media and downloaded_media.is_ocr_supported:
            ocr_content = self.ocr_engine.run(file_path=downloaded_media.disk_file_path)
            if ocr_content:
                ocr_content = '====OCR CONTENT====\n' + ocr_content

        # Create Dict with All Value
        values: Dict = {
            'id': message.id,
            'group_id': event.chat.id,
            'date_time': message.date.astimezone(tz=pytz.utc),
            'message': self.__build_final_message(message.message, ocr_content),
            'raw': self.__build_final_message(message.raw_text, ocr_content),
            'to_id': message.to_id.channel_id if message.to_id is not None and hasattr(message.to_id, 'channel_id') else None,
            'media_id': downloaded_media.media_id if downloaded_media else None,
            'is_reply': message.is_reply,
            'reply_to_msg_id': message.reply_to.reply_to_msg_id if message.is_reply else None,
        }

        # Process Sender ID
        if message.from_id is not None:
            if isinstance(message.from_id, PeerUser):

                values['from_id'] = message.from_id.user_id
                values['from_type'] = 'User'

                # Ensure User Exists
                await self.__ensure_user_exists(event=event)

            else:
                values['from_id'] = None
                values['from_type'] = None

        # Execute Finder
        await self.finder.run(
            await TelethonMessageEntityMapper.to_finder_notification_facade_entity(
                message=message,
                downloaded_media_info=downloaded_media,
                ocr_content=ocr_content),
            source=self.target_phone_number,
        )

        # Add to DB
        TelegramMessageDatabaseManager.insert(values)

        # Update Signals Engine
        self.signals_engine.inc_messages_sent()

    def __build_final_message(self, message: str, ocr_data: Optional[str]) -> str:
        """Compute Final Message for Dict."""
        h_result: str = ''

        if message:
            h_result += message

        if ocr_data:
            if message and message != '':
                h_result += '\n\n'
            h_result += ocr_data

        return h_result

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
            result: Optional[User] = None
            try:
                result = await event.get_sender()
            except ChannelPrivateError as _ex:
                logger.warning(
                    f'\t\tUnable to resolve User "{event.from_id.user_id}" due privacy restrictions')

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
                f'\t\tGroup "{event.chat.id}" not found on DB. Performing automatic synchronization. Consider execute '
                f'"load_groups" command to perform a full group synchronization (Members and Group Cover Photo).',
            )

            # Retrieve Group Definitions
            result: Channel = await event.get_chat()

            # Perform Synchronization
            if result:
                group_dict_data: Dict = TelethonChannelEntityMapper.to_database_dict(
                    entity=result,
                    target_phone_numer=self.target_phone_number,
                )

                TelegramGroupDatabaseManager.insert_or_update(group_dict_data)

                # Send Signal
                await self.signals_engine.new_group(
                    group_id=str(group_dict_data['id']),
                    group_title=group_dict_data['title'],
                )

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not await self.can_activate(config, args, data):
            logger.debug('\t\tModule is Not Enabled...')
            return

        # Update Module Global Info
        self.download_media = not args['ignore_media']
        self.data_path = config['CONFIGURATION']['data_path']
        self.target_phone_number = config['CONFIGURATION']['phone_number']

        try:
            # Attach Termination Signals
            signal.signal(signal.SIGINT, self.__handle_term_signal)  # type: ignore
            signal.signal(signal.SIGTERM, self.__handle_term_signal)  # type: ignore

            # Set Notification Engines
            self.notification_engine.configure(config=config)

            # Set Data Export Engines
            self.exporter_engine.configure(config=config)

            # Set Finder
            self.finder.configure(
                config=config,
                notification_engine=self.notification_engine,
                exporter_engine=self.exporter_engine,
            )

            # Setup Media Handler
            self.media_handler.configure(config=config)

            # Set OCR Engine
            self.ocr_engine = OcrEngineFactory.get_instance(config=config)

            # Set Keep Alive Settings
            self.signals_engine = SignalsEngineFactory.get_instance(
                config=config,
                notification_engine=self.notification_engine,
                source=self.target_phone_number,
            )

        except AttributeError as ex:
            logger.fatal(ex)
            data['internals']['panic'] = True
            return

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

        # Send Init Signal
        await self.signals_engine.init()

        # Loop Until Signal Termination
        while not self.term_signal:

            if client.is_connected():
                self.sleep_task = asyncio.create_task(self.__sleep())
                await self.sleep_task

            else:
                break  # Future: Handle Reconnection + Configure Reconnection in config file

            # Send Keep-Alive Signal
            await self.signals_engine.keep_alive()

        # Disconnect Telegram Client
        await self.__disconnect(client=client)

        # Shutdown All Exporters
        await self.__shutdown_exporters()

    async def __shutdown_exporters(self) -> None:
        """Shutdown all Exporters."""
        logger.info('\t\tShutdown File Exporters...')
        await self.exporter_engine.shutdown()

    async def __disconnect(self, client: TelegramClient) -> None:
        """Disconnect Telegram Client."""
        # Disconnect the Client
        client.disconnect()

        # Wait Disconnect
        while client.is_connected():
            logger.info('\t\tWaiting Client Disconnection...')
            await asyncio.sleep(1)

        logger.info('\t\tTelegram Client Disconnected...')

        # Send Shutdown Signal
        await self.signals_engine.shutdown()

    async def __sleep(self) -> None:
        """Allow Sleep Function to be Canceled."""
        with contextlib.suppress(asyncio.CancelledError):
            await asyncio.sleep(self.signals_engine.keep_alive_interval)

