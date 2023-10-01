"""Finder Engine."""
from configparser import ConfigParser
from typing import Dict, List

from telethon.events import NewMessage

from TEx.finder.regex_finder import RegexFinder
from TEx.notifier.notifier_engine import NotifierEngine


class FinderEngine:
    """Primary Finder Engine."""

    def __init__(self) -> None:
        """Initialize Finder Engine."""
        self.is_finder_enabled: bool = False
        self.rules: List[Dict] = []
        self.notification_engine: NotifierEngine = NotifierEngine()

    def __is_finder_enabled(self, config: ConfigParser) -> bool:
        """Check if Finder Module is Enabled."""
        return (
            config.has_option('FINDER', 'enabled') and config['FINDER']['enabled'] == 'true'
            )

    def __load_rules(self, config: ConfigParser) -> None:
        """Load Finder Rules."""
        rules_sections: List[str] = [item for item in config.sections() if 'FINDER.RULE.' in item]

        for sec in rules_sections:
            if config[sec]['type'] == 'regex':
                self.rules.append({
                    'id': sec,
                    'instance': RegexFinder(config=config[sec]),
                    'notifier': config[sec]['notifier']
                    })

    def configure(self, config: ConfigParser) -> None:
        """Configure Finder."""
        self.is_finder_enabled = self.__is_finder_enabled(config=config)
        self.__load_rules(config=config)
        self.notification_engine.configure(config=config)

    async def run(self, message: NewMessage.Event) -> None:
        """Execute the Finder with Raw Text."""
        if not self.is_finder_enabled:
            return

        for rule in self.rules:
            is_found: bool = await rule['instance'].find(raw_text=message.raw_text)

            if is_found:

                # Runt the Notification Engine
                await self.notification_engine.run(
                    notifiers=rule['notifier'].split(','),
                    message=message,
                    rule_id=rule['id']
                    )
