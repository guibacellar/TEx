"""Facade Entities for Signal based Notifications."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SignalNotificationEntityModel(BaseModel):
    """Facade Entities for Signal based Notifications."""

    model_config = ConfigDict(extra='forbid')

    signal: str
    date_time: datetime
    content: str
