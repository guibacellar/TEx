"""Signal Entity."""
from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, ConfigDict


class SignalEntity(BaseModel):
    """Signal Entity."""

    model_config = ConfigDict(extra='forbid')

    enabled: bool
    keep_alive_interval: int
    notifiers: Dict
