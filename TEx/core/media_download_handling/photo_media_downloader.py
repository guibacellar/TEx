"""Photo Media Downloader."""
import os
from typing import Dict

from telethon.tl.types import Message


class PhotoMediaDownloader:
    """Photo Media Downloader."""

    @staticmethod
    async def download(message: Message, media_metadata: Dict, data_path: str) -> None:
        """Download the Media and Update MetadaInfo.

        :param message:
        :param media_metadata:
        :return:
        """
        # Download Media
        await message.download_media(os.path.join(data_path, media_metadata['file_name']))
