"""Regex Finder."""
from __future__ import annotations

import re
from configparser import SectionProxy
from typing import List

from TEx.finder.base_finder import BaseFinder


class RegexFinder(BaseFinder):
    """Regex Based Finder."""

    def __init__(self, config: SectionProxy) -> None:
        """Initialize RegEx Finder."""
        raw_regex_content: str = config['regex']
        regex_conf_list: List[str] = [
            item for item in raw_regex_content.split('\n') if item and item != ''
        ] if '\n' in raw_regex_content else [raw_regex_content]

        self.regex_patterns: List[re.Pattern] = [
            re.compile(regex_conf, flags=re.IGNORECASE | re.MULTILINE) for regex_conf in regex_conf_list
        ]

    async def find(self, raw_text: str) -> bool:
        """Apply Find Logic."""
        if not raw_text or len(raw_text) == 0:
            return False

        return any(len(pattern.findall(raw_text)) > 0 for pattern in self.regex_patterns)
