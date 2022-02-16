"""Standard Media Downloader."""
import base64
import os
from typing import Dict, List

from telethon.tl.types import Message


class StandardMediaDownloader:
    """Standard Media Downloader."""

    @staticmethod
    async def download(message: Message, media_metadata: Dict, data_path: str) -> None:
        """Download the Media and Update MetadaInfo.

        :param message:
        :param media_metadata:
        :return:
        """
        if not media_metadata:
            return None

        # Download Media
        target_path: str = os.path.join(data_path, 'download', StandardMediaDownloader.sanitize_media_filename(media_metadata["file_name"]))
        generated_path: str = await message.download_media(target_path)
        media_metadata['extension'] = os.path.splitext(generated_path)[1]

        # Get File Content
        with open(generated_path, 'rb') as file:
            media_metadata['b64_content'] = base64.b64encode(file.read()).decode()
            file.close()

        # Remove File
        os.remove(generated_path)

    @staticmethod
    def sanitize_media_filename(filename: str) -> str:
        """Sanitize Media Filename."""

        sanit_charts: List[str] = [char for char in filename if not char.isalpha() and char != ' ' and not char.isalnum() and char != '.' and char != '-']
        h_result: str = filename

        for sanit_item in sanit_charts:
            h_result = h_result.replace(sanit_item, '_')

        return h_result