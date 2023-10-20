"""All Messages Finder."""
from configparser import SectionProxy

from TEx.finder.base_finder import BaseFinder


class AllMessagesFinder(BaseFinder):
    """All Messages Based Finder."""

    def __init__(self, config: SectionProxy) -> None:
        """Initialize All Messages Finder."""

    async def find(self, raw_text: str) -> bool:
        """Find Message. Always Return True."""
        return True
