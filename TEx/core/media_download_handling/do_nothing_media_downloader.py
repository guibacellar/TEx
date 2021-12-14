"""Do Nothing Media Downloader."""
from typing import Dict

from telethon.tl.types import Message


class DoNothingMediaDownloader:
    """Do Nothing Media Downloader."""

    @staticmethod
    async def download(message: Message, media_metadata: Dict, data_path: str) -> None:  # pylint: disable=W0613
        """Download the Media, Update MetadaInfo and Return the ID from DB Record.

        :param message:
        :param media_metadata:
        :return:
        """
        return None
