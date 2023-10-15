"""Elastic Search Notifier."""
from __future__ import annotations

from configparser import SectionProxy
from typing import Dict, Optional

import pytz
from elasticsearch import AsyncElasticsearch
from telethon.events import NewMessage
from telethon.tl.types import PeerUser

from TEx.notifier.notifier_base import BaseNotifier


class ElasticSearchNotifier(BaseNotifier):
    """Basic Elastic Search Notifier."""

    def __init__(self) -> None:
        """Initialize Elastic Search Notifier."""
        super().__init__()
        self.url: str = ''
        self.client: AsyncElasticsearch = None
        self.index: str = ''
        self.pipeline: str = ''

    def configure(self, config: SectionProxy) -> None:
        """Configure the Notifier."""
        hosts_list: Optional[str] = config.get('address', fallback=None)

        self.client = AsyncElasticsearch(
            hosts=hosts_list.split(',') if hosts_list else None,
            api_key=config.get('api_key', fallback=None),
            verify_certs=config.get('verify_ssl_cert', fallback='True') == 'True',
            cloud_id=config.get('cloud_id', fallback=None),
        )
        self.index = config['index_name']
        self.pipeline = config['pipeline_name']

    async def run(self, message: NewMessage.Event, rule_id: str) -> None:
        """Run Elastic Search Notifier."""
        content: Dict = {
                'time': message.date.astimezone(tz=pytz.utc),
                'rule': rule_id,
                'raw': message.raw_text,
                'group_name': message.chat.title,
                'group_id': message.chat.id,
                'from_id': message.from_id.user_id if isinstance(message.from_id, PeerUser) else '',
                'to_id': message.to_id.channel_id if message.to_id is not None else None,
                'reply_to_msg_id': message.reply_to.reply_to_msg_id if message.is_reply else None,
                'message_id': message.id,
                'is_reply': message.is_reply,
            }

        if hasattr(message, 'file') and message.file:
            content['has_media'] = True
            content['media_mime_type'] = message.file.mime_type if hasattr(message.file, 'mime_type') else None
            content['media_size'] = message.file.size if hasattr(message.file, 'size') else None
        else:
            content['has_media'] = False
            content['media_mime_type'] = None
            content['media_size'] = None

        await self.client.index(
            index=self.index,
            pipeline=self.pipeline,
            id=f'{message.chat.id}_{message.id}',
            document=content,
        )
