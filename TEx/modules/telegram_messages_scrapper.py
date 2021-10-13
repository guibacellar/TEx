"""Telegram Group Scrapper."""
import asyncio
import logging
import threading
from configparser import ConfigParser
from time import sleep
from typing import Dict, List, Optional

import pytz
from telethon import TelegramClient
from telethon.tl.types import (Message, MessageMediaDocument, MessageMediaGeo, MessageMediaPhoto, MessageMediaWebPage,
                               MessageService, PeerUser)

from TEx.core.base_module import BaseModule
from TEx.core.media_download_handling.do_nothing_media_downloader import DoNothingMediaDownloader
from TEx.core.media_download_handling.photo_media_downloader import PhotoMediaDownloader
from TEx.core.media_download_handling.std_media_downloader import StandardMediaDownloader
from TEx.core.media_metadata_handling.do_nothing_media_handler import DoNothingHandler
from TEx.core.media_metadata_handling.generic_binary_handler import GenericBinaryMediaHandler
from TEx.core.media_metadata_handling.geo_handler import GeoMediaHandler
from TEx.core.media_metadata_handling.mp4_handler import MediaMp4Handler
from TEx.core.media_metadata_handling.pdf_handler import PdfMediaHandler
from TEx.core.media_metadata_handling.photo_handler import PhotoMediaHandler
from TEx.core.media_metadata_handling.sticker_handler import MediaStickerHandler
from TEx.core.media_metadata_handling.text_handler import TextPlainHandler
from TEx.core.media_metadata_handling.webimage_handler import WebImageStickerHandler
from TEx.database.TelegramGroupDatabase import TelegramGroupDatabaseManager, TelegramMediaDatabaseManager, \
    TelegramMessageDatabaseManager
from TEx.models.database.telegram_db_model import TelegramGroupOrmEntity

logger = logging.getLogger()


class TelegramGroupMessageScrapper(BaseModule):
    """Download all Messages from Telegram Groups."""

    __MEDIA_HANDLERS: Dict = {
        'video/mp4': {
            'metadata_handler': MediaMp4Handler.handle_metadata,
            'downloader': StandardMediaDownloader.download
            },
        'application/x-tgsticker': {
            'metadata_handler': MediaStickerHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download
            },
        'image/webp': {
            'metadata_handler': WebImageStickerHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download
            },
        'text/plain': {
            'metadata_handler': TextPlainHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download
            },
        'photo': {
            'metadata_handler': PhotoMediaHandler.handle_metadata,
            'downloader': PhotoMediaDownloader.download
            },
        'application/pdf': {
            'metadata_handler': PdfMediaHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download
            },
        'application/x-ms-dos-executable': {
            'metadata_handler': GenericBinaryMediaHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download
            },
        'application/vnd.android.package-archive': {
            'metadata_handler': GenericBinaryMediaHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download
            },
        'application/vnd.generic.binary': {
            'metadata_handler': GenericBinaryMediaHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download
            },
        'geo': {
            'metadata_handler': GeoMediaHandler.handle_metadata,
            'downloader': DoNothingMediaDownloader.download
            },
        'do_nothing': {
            'metadata_handler': DoNothingHandler.handle_metadata,
            'downloader': DoNothingMediaDownloader.download
            }
        }

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not args['download_messages']:
            logger.info('\t\tModule is Not Enabled...')
            return

        # Get Client
        client: TelegramClient = data['telegram_client']

        # Load Groups from DB
        groups: List[TelegramGroupOrmEntity] = TelegramGroupDatabaseManager.get_all_by_phone_number(
            args['target_phone_number'])
        logger.info(f'\t\tFound {len(groups)} Groups')

        for group in groups:
            try:
                await self.download_messages(
                    group_id=group.id,
                    client=client,
                    group_name=group.title,
                    download_media=not args['ignore_media']
                )
            except ValueError as ex:
                logger.info('\t\t\tUnable to Download Messages...')
                logger.error(ex)

    async def download_messages(self, group_id: int, group_name: str, client: TelegramClient, download_media: bool) -> None:
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
                    group_id,
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
                    'media_id': await self.handle_medias(message) if download_media else None
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

    async def handle_medias(self, message: Message) -> Optional[int]:
        """Handle Message Media, Photo, File, etc."""
        executor_id: str = 'not_defined'

        if message.voice is not None:
            executor_id = 'do_nothing'

        elif message.media is not None:
            if isinstance(message.media, MessageMediaWebPage):
                executor_id = 'do_nothing'

            elif isinstance(message.media, MessageMediaDocument):
                logger.info(
                    f'\t\t\tDownloading Media from Message {message.id} ({message.media.document.size / 1024:.6} Kbytes) as {message.media.document.mime_type}')
                executor_id = message.media.document.mime_type

            elif isinstance(message.media, MessageMediaGeo):
                logger.info(f'\t\t\tDownloading Geo from Message {message.id}')
                executor_id = 'geo'

            elif isinstance(message.media, MessageMediaPhoto):
                logger.info(f'\t\t\tDownloading Photo from Message {message.id}')
                executor_id = 'photo'

            else:
                logger.info(f'\t\t\tNot Supported Media Type {type(message.media)}. Ignoring...')
                return None

        if executor_id == 'not_defined':
            return None

        # Retrieve the Executor Spec
        executor_spec: Dict = {}
        if executor_id in TelegramGroupMessageScrapper.__MEDIA_HANDLERS:
            executor_spec = TelegramGroupMessageScrapper.__MEDIA_HANDLERS[executor_id]
        else:
            executor_spec = TelegramGroupMessageScrapper.__MEDIA_HANDLERS['application/vnd.generic.binary']

        # Get Media Metadata
        media_metadata: Optional[Dict] = executor_spec['metadata_handler'](
            message=message
            )

        # Download Media and Save into DB
        await executor_spec['downloader'](
            message=message,
            media_metadata=media_metadata
            )

        # Update into DB
        if media_metadata is not None:
            return TelegramMediaDatabaseManager.insert(media_metadata)

        return None
