"""Facade Entities for Finder e Notification Engine Modules."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from TEx.models.facade.media_handler_facade_entity import MediaHandlingEntity


class FinderNotificationMessageEntity(BaseModel):
    """Facade Entity for Finder and Notification."""

    model_config = ConfigDict(extra='forbid')

    date_time: datetime
    raw_text: str
    group_name: Optional[str]
    group_id: Optional[int]
    from_id: Optional[int]
    to_id: Optional[int]
    reply_to_msg_id: Optional[int]
    message_id: Optional[int]
    is_reply: Optional[bool]
    downloaded_media_info: Optional[MediaHandlingEntity]
    found_on: str
