"""Base Class for All Finders."""
from __future__ import annotations

import abc


class BaseFinder:
    """Base Finder Class."""

    @abc.abstractmethod
    async def find(self, raw_text: str) -> bool:
        """Apply Find Logic."""
