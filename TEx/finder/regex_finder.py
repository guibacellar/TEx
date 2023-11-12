"""Regex Finder."""
import re
from configparser import SectionProxy

from TEx.finder.base_finder import BaseFinder


class RegexFinder(BaseFinder):
    """Regex Based Finder."""

    def __init__(self, config: SectionProxy) -> None:
        """Initialize RegEx Finder."""
        self.regex: re.Pattern = re.compile(config['regex'], flags=re.IGNORECASE | re.MULTILINE)

    async def find(self, raw_text: str) -> bool:
        """Apply Find Logic."""
        return len(self.regex.findall(raw_text)) > 0 if raw_text else False
