"""Do Nothing Media Downloader."""
from __future__ import annotations

from typing import Dict

from telethon.tl.patched import Message


class DoNothingMediaDownloader:
    """Do Nothing Media Downloader."""

    @staticmethod
    async def download(message: Message, media_metadata: Dict, data_path: str) -> None:
        """Download the Media, Update MetadaInfo and Return the ID from DB Record.

        :param message:
        :param media_metadata:
        :return:
        """
        return
