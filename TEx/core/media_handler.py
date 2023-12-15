"""Universal Telegram Media Handler."""
from __future__ import annotations

import hashlib
import logging
import os
from configparser import ConfigParser
from typing import Dict, List, Optional

from telethon.tl.types import Message, MessageMediaDocument, MessageMediaGeo, MessageMediaPhoto, MessageMediaWebPage

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
from TEx.models.facade.media_handler_facade_entity import MediaHandlingEntity

logger = logging.getLogger('TelegramExplorer')


class UniversalTelegramMediaHandler:
    """Handle all Media Complexity for Download or Persistence."""

    __MAX_DOWNLOAD_SIZE_BYTES: int = 256000000  # 256 MB

    __IMAGE_OCR_MIME_TYPES: List[str] = [
        'image/bmp', 'image/cis-cod', 'image/gif', 'image/ief', 'image/jpeg', 'image/pipeg', 'image/png',
        'image/tiff', 'image/x-cmu-raster', 'image/x-cmx', 'image/x-icon', 'image/x-portable-anymap',
        'image/x-portable-bitmap', 'image/x-portable-graymap', 'image/x-portable-pixmap', 'image/x-rgb',
        'image/x-xbitmap', 'image/x-xpixmap', 'image/x-xwindowdump', 'image/x-jg', 'image/vnd.microsoft.icon',
        'image/x-bmp', 'image/x-ms-bmp', 'image/svg+xml', 'image/webp',
    ]

    __MEDIA_HANDLERS: Dict = {
        'video/mp4': {
            'metadata_handler': MediaMp4Handler.handle_metadata,
            'downloader': StandardMediaDownloader.download,
            },
        'application/x-tgsticker': {
            'metadata_handler': MediaStickerHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download,
            },
        'image/webp': {
            'metadata_handler': WebImageStickerHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download,
            },
        'text/plain': {
            'metadata_handler': TextPlainHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download,
            },
        'photo': {
            'metadata_handler': PhotoMediaHandler.handle_metadata,
            'downloader': PhotoMediaDownloader.download,
            },
        'application/pdf': {
            'metadata_handler': PdfMediaHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download,
            },
        'application/x-ms-dos-executable': {
            'metadata_handler': GenericBinaryMediaHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download,
            },
        'application/vnd.android.package-archive': {
            'metadata_handler': GenericBinaryMediaHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download,
            },
        'application/vnd.generic.binary': {
            'metadata_handler': GenericBinaryMediaHandler.handle_metadata,
            'downloader': StandardMediaDownloader.download,
            },
        'geo': {
            'metadata_handler': GeoMediaHandler.handle_metadata,
            'downloader': DoNothingMediaDownloader.download,
            },
        'do_nothing': {
            'metadata_handler': DoNothingHandler.handle_metadata,
            'downloader': DoNothingMediaDownloader.download,
            },
        }

    def __init__(self) -> None:
        """Class Initialization."""
        self.default_mode: str = ''
        self.default_max_download_size_bytes: int = 0
        self.mime_type_mapping: Dict = {}

    def configure(self, config: ConfigParser) -> None:
        """Configure Media Parser."""
        self.default_mode = config.get('MEDIA.DOWNLOAD', 'default', fallback='DISALLOW')
        self.default_max_download_size_bytes = int(
            config.get('MEDIA.DOWNLOAD',
                       'max_download_size_bytes',
                       fallback=UniversalTelegramMediaHandler.__MAX_DOWNLOAD_SIZE_BYTES),
            )

        # Get Specific Mappings
        specific_keys: List[str] = [item for item in config.sections() if 'MEDIA.DOWNLOAD.' in item]
        for key in specific_keys:
            self.mime_type_mapping[key.replace('MEDIA.DOWNLOAD.', '')] = {
                'enabled': config.get(key, 'enabled', fallback='DISALLOW'),
                'max_download_size_bytes': int(
                    config.get(key,
                               'max_download_size_bytes',
                               fallback=UniversalTelegramMediaHandler.__MAX_DOWNLOAD_SIZE_BYTES),
                    ),
                'groups': config.get(key, 'groups', fallback='*').split(','),
            }

    async def handle_medias(self, message: Message, group_id: int, data_path: str) -> Optional[MediaHandlingEntity]:
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
            message=message,
            )

        # Handle Unicode Chars on Media File Name - TODO: TO Method
        if media_metadata and media_metadata['file_name']:
            try:
                media_metadata['file_name'] = f"{message.id}_{media_metadata['file_name']}"
                media_metadata['file_name'].encode('ascii')
            except UnicodeError:
                file, ext = os.path.splitext(media_metadata['file_name'])
                media_metadata['file_name'] = f'{hashlib.md5(file.encode("utf-8")).hexdigest()}{ext}'

        # Check if Can Download Media
        allow_download: bool = self.check_if_allow_download(media_metadata, group_id=str(group_id))
        if not allow_download and media_metadata:
            logger.info('\t\t\t\tMedia Download is not Allowed, Ignoring...')
            return None

        # Download Media
        target_file_path: str = os.path.join(data_path, 'media', str(group_id))
        await executor_spec['downloader'](
            message=message,
            media_metadata=media_metadata,
            data_path=target_file_path,
            )

        # Update Reference into DB
        if media_metadata is not None:
            media_metadata['group_id'] = group_id
            media_id: int = TelegramMediaDatabaseManager.insert(entity_values=media_metadata)

            return MediaHandlingEntity(
                media_id=media_id,
                file_name=media_metadata['file_name'],
                content_type=media_metadata['mime_type'],
                size_bytes=media_metadata['size_bytes'],
                disk_file_path=os.path.join(target_file_path, media_metadata['file_name']),
                is_ocr_supported=media_metadata['mime_type'] in UniversalTelegramMediaHandler.__IMAGE_OCR_MIME_TYPES,
            )

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
                    f'\t\t\tDownloading Media from Message {message.id} ({message.media.document.size / 1024:.6} Kbytes)'
                    f' as {message.media.document.mime_type} at {message.date.strftime("%Y-%m-%d %H:%M:%S")}',
                    )
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

    def check_if_allow_download(self, media_metadata: Optional[Dict], group_id: str) -> bool:
        """Check if Media Download are Allowed."""
        if not media_metadata or \
                'size_bytes' not in media_metadata or \
                not media_metadata['size_bytes']:
            return False

        # Check Download Settings
        mime_type: Optional[str] = media_metadata.get('mime_type')

        if mime_type and mime_type in self.mime_type_mapping:

            map_element: Dict = self.mime_type_mapping[mime_type]
            h_result: bool = map_element['enabled'] == 'ALLOW' and \
                media_metadata['size_bytes'] <= map_element['max_download_size_bytes'] and \
                (map_element['groups'] == ['*'] or group_id in map_element['groups'])
            return h_result

        # Fallback for non-Configured Mime Type
        return self.default_mode == 'ALLOW' and media_metadata['size_bytes'] <= self.default_max_download_size_bytes
