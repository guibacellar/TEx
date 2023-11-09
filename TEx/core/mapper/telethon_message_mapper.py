"""Telethon Event Entity Mapper."""
from __future__ import annotations

import logging
from typing import Optional, Union

from pydantic import BaseModel
from telethon.errors import ChannelPrivateError
from telethon.tl.patched import Message
from telethon.tl.types import Channel, Chat, PeerUser, User

from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.models.facade.media_handler_facade_entity import MediaHandlingEntity

logger = logging.getLogger('TelegramExplorer')


class TelethonMessageEntityMapper:
    """Telethon Event Entity Mapper."""

    class ChatPropsModel(BaseModel):
        """Model for __map_chat_props method."""

        chat_id: int
        chat_title: str

    @staticmethod
    async def to_finder_notification_facade_entity(message: Message, downloaded_media_info: Optional[MediaHandlingEntity], ocr_content: Optional[str]) -> \
    Optional[FinderNotificationMessageEntity]:
        """Map Telethon Event to FinderNotificationMessageEntity."""
        if not message:
            return None

        try:
            mapped_chat_props: TelethonMessageEntityMapper.ChatPropsModel = TelethonMessageEntityMapper.__map_chat_props(
                entity=await message.get_chat(),
            )
        except ChannelPrivateError as _ex:
            return None

        raw_text: str = message.raw_text
        if ocr_content:
            if raw_text and raw_text != '':
                raw_text += '\n\n'

            raw_text += ocr_content

        h_result: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=message.date,
            raw_text=raw_text,
            group_name=mapped_chat_props.chat_title,
            group_id=mapped_chat_props.chat_id,
            from_id=message.from_id.user_id if isinstance(message.from_id, PeerUser) else None,
            to_id=message.to_id.channel_id if message.to_id is not None and hasattr(message.to_id, 'channel_id') else None,
            reply_to_msg_id=message.reply_to.reply_to_msg_id if message.is_reply and message.reply_to else None,
            message_id=message.id,
            is_reply=message.is_reply,
            downloaded_media_info=downloaded_media_info,
            found_on='UNDEFINED',
        )

        return h_result

    @staticmethod
    def __map_chat_props(entity: Union[Channel, User, Chat]) -> TelethonMessageEntityMapper.ChatPropsModel:
        """Map Chat Specific Props."""
        if isinstance(entity, (Channel, Chat)):
            return TelethonMessageEntityMapper.ChatPropsModel(
                chat_id=entity.id,
                chat_title=entity.title if entity.title else '',
            )

        if isinstance(entity, User):
            return TelethonMessageEntityMapper.ChatPropsModel(
                chat_id=entity.id,
                chat_title=entity.username if entity.username else (entity.phone if entity.phone else ''),
            )

        raise AttributeError(entity, 'Invalid entity type: ' + str(type(entity)))
