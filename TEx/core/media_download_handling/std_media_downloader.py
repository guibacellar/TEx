"""Standard Media Downloader."""
import base64
import os
from typing import Dict

from telethon.tl.types import Message


class StandardMediaDownloader:
    """Standard Media Downloader."""

    @staticmethod
    async def download(message: Message, media_metadata: Dict) -> None:
        """Download the Media and Update MetadaInfo.

        :param message:
        :param media_metadata:
        :return:
        """
        if not media_metadata:
            return None

        # Download Media
        generated_path: str = await message.download_media(f'data/download/{media_metadata["file_name"]}')
        media_metadata['extension'] = os.path.splitext(generated_path)[1]

        # Get File Content
        with open(generated_path, 'rb') as file:
            media_metadata['b64_content'] = base64.b64encode(file.read()).decode()
            file.close()

        # Remove File
        os.remove(generated_path)
