"""Base Class for All Finders."""
import abc


class BaseFinder:
    """Base Finder Class."""

    @abc.abstractmethod
    async def find(self, raw_text: str) -> bool:
        """Apply Find Logic."""
