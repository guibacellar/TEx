"""Photo Media Downloader."""
import base64
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
        generated_path: str = await message.download_media(f'{data_path}/download/')
        media_metadata['extension'] = os.path.splitext(generated_path)[1]
        media_metadata['file_name'] = os.path.basename(generated_path)
        media_metadata['mime_type'] = f'image/{media_metadata["extension"][1:]}'

        # Get File Content
        with open(generated_path, 'rb') as file:
            content: bytes = file.read()
            media_metadata['b64_content'] = base64.b64encode(content).decode()
            media_metadata['size_bytes'] = len(content)
            file.close()

        # Remove File
        os.remove(generated_path)
