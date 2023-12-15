"""Elastic Search Notifier."""
from __future__ import annotations

from configparser import SectionProxy
from typing import Dict, Optional, Union

import pytz
from elasticsearch import AsyncElasticsearch

from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.models.facade.signal_notification_model import SignalNotificationEntityModel
from TEx.notifier.notifier_base import BaseNotifier


class ElasticSearchNotifier(BaseNotifier):
    """Basic Elastic Search Notifier."""

    def __init__(self) -> None:
        """Initialize Elastic Search Notifier."""
        super().__init__()
        self.url: str = ''
        self.client: Optional[AsyncElasticsearch] = None
        self.index: str = ''
        self.pipeline: str = ''

    def configure(self, config: SectionProxy) -> None:
        """Configure the Notifier."""
        hosts_list: Optional[str] = config.get('address', fallback=None)

        self.client = AsyncElasticsearch(
            hosts=hosts_list.split(',') if hosts_list else None,  # type: ignore
            api_key=config.get('api_key', fallback=None),
            verify_certs=config.get('verify_ssl_cert', fallback='True') == 'True',
            cloud_id=config.get('cloud_id', fallback=None),
            request_timeout=30,
            max_retries=10,
            ssl_show_warn=False,
        )
        self.index = config['index_name']
        self.pipeline = config['pipeline_name']

    async def run(self, entity: Union[FinderNotificationMessageEntity, SignalNotificationEntityModel], rule_id: str, source: str) -> None:
        """Run Elastic Search Notifier."""
        if not self.client:
            return

        content: Dict

        if isinstance(entity, FinderNotificationMessageEntity):
            content = await self.__get_dict_for_finder_notification(
                entity=entity,
                rule_id=rule_id,
                source=source,
            )
        else:
            content = await self.__get_dict_for_signal_notification(
                entity=entity,
                source=source,
            )

        await self.client.index(
            index=self.index,
            pipeline=self.pipeline,
            document=content,
        )

    async def __get_dict_for_finder_notification(self, entity: FinderNotificationMessageEntity, rule_id: str, source: str) -> Dict:
        """Return the Dict for Finder Notifications."""
        content: Dict = {
                'time': entity.date_time.astimezone(tz=pytz.utc),
                'source': source,
                'rule': rule_id,
                'raw': entity.raw_text,
                'group_name': entity.group_name,
                'group_id': entity.group_id,
                'from_id': entity.from_id,
                'to_id': entity.to_id,
                'reply_to_msg_id': entity.reply_to_msg_id,
                'message_id': entity.message_id,
                'is_reply': entity.is_reply,
                'found_on': entity.found_on,
            }

        if entity.downloaded_media_info:
            content['has_media'] = True
            content['media_mime_type'] = entity.downloaded_media_info.content_type
            content['media_size'] = entity.downloaded_media_info.size_bytes
        else:
            content['has_media'] = False
            content['media_mime_type'] = None
            content['media_size'] = None

        return content

    async def __get_dict_for_signal_notification(self, entity: SignalNotificationEntityModel, source: str) -> Dict:
        """Return the Dict for Signal Notifications."""
        content: Dict = {
            'time': entity.date_time.astimezone(tz=pytz.utc),
            'source': source,
            'signal': entity.signal,
            'content': entity.content,
        }

        return content

