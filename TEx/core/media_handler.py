"""Universal Telegram Media Handler."""
import hashlib
import logging
import os

from typing import Dict, Optional

from telethon.tl.types import (Message,
                               MessageMediaDocument,
                               MessageMediaGeo,
                               MessageMediaPhoto,
                               MessageMediaWebPage)

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
from TEx.database.telegram_group_database import TelegramMediaDatabaseManager


logger = logging.getLogger()


class UniversalTelegramMediaHandler:
    """Handle all Media Complexity for Download or Persistence."""

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

    async def handle_medias(self, message: Message, group_id: int, data_path: str) -> Optional[int]:
        """Handle Message Media, Photo, File, etc."""
        executor_id: Optional[str] = self.__resolve_executor_id(message=message)

        if executor_id == 'not_defined':
            return None

        # Retrieve the Executor Spec
        executor_spec: Dict = {}
        if executor_id in UniversalTelegramMediaHandler.__MEDIA_HANDLERS:
            executor_spec = UniversalTelegramMediaHandler.__MEDIA_HANDLERS[executor_id]
        else:
            executor_spec = UniversalTelegramMediaHandler.__MEDIA_HANDLERS['application/vnd.generic.binary']

        # Get Media Metadata
        media_metadata: Optional[Dict] = executor_spec['metadata_handler'](
            message=message
            )

        # Handle Unicode Chars on Media File Name - TODO: TO Method
        if media_metadata and media_metadata['file_name']:
            try:
                media_metadata['file_name'] = f"{message.id}_{media_metadata['file_name']}"
                media_metadata['file_name'].encode('ascii')
            except UnicodeError:
                file, ext = os.path.splitext(media_metadata['file_name'])
                media_metadata['file_name'] = f'{hashlib.md5(file.encode("utf-8")).hexdigest()}{ext}'  # nosec

        # Check Media Size - TODO: TO Method
        if media_metadata and \
                'size_bytes' in media_metadata and \
                media_metadata['size_bytes'] and \
                media_metadata['size_bytes'] > 256000000:  # 256 MB
            logger.info('\t\t\t\tMedia too Large. Ignoring...')
            return None

        # Download Media
        target_file_path: str = os.path.join(data_path, 'media', str(group_id))
        await executor_spec['downloader'](
            message=message,
            media_metadata=media_metadata,
            data_path=target_file_path
            )

        # Update Reference into DB
        if media_metadata is not None:
            media_metadata['group_id'] = group_id
            return TelegramMediaDatabaseManager.insert(entity_values=media_metadata)

        return None

    def __resolve_executor_id(self, message: Message) -> Optional[str]:
        """Resolve the Executor ID."""
        executor_id: str = 'not_defined'

        if message.voice is not None:
            executor_id = 'do_nothing'

        elif message.media is not None:
            if isinstance(message.media, MessageMediaWebPage):
                executor_id = 'do_nothing'

            elif isinstance(message.media, MessageMediaDocument):
                logger.info(
                    f'\t\t\tDownloading Media from Message {message.id} ({message.media.document.size / 1024:.6} Kbytes) as {message.media.document.mime_type} at {message.date.strftime("%Y-%m-%d %H:%M:%S")}')
                executor_id = message.media.document.mime_type

            elif isinstance(message.media, MessageMediaGeo):
                logger.info(f'\t\t\tDownloading Geo from Message {message.id}')
                executor_id = 'geo'

            elif isinstance(message.media, MessageMediaPhoto):
                logger.info(f'\t\t\tDownloading Photo from Message {message.id} at {message.date.strftime("%Y-%m-%d %H:%M:%S")}')
                executor_id = 'photo'

            else:
                logger.info(f'\t\t\tNot Supported Media Type {type(message.media)}. Ignoring...')

        return executor_id
