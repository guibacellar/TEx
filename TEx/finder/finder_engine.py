"""Finder Engine."""
from __future__ import annotations

from configparser import ConfigParser, SectionProxy
from typing import Dict, List, Optional

import aiofiles
import aiofiles.os

from TEx.exporter.exporter_engine import ExporterEngine
from TEx.finder.all_messages_finder import AllMessagesFinder
from TEx.finder.base_finder import BaseFinder
from TEx.finder.regex_finder import RegexFinder
from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.notifier.notifier_engine import NotifierEngine


class FinderEngine:
    """Primary Finder Engine."""

    def __init__(self) -> None:
        """Initialize Finder Engine."""
        self.is_finder_enabled: bool = False
        self.rules: List[Dict] = []
        self.notification_engine: NotifierEngine
        self.exporter_engine: ExporterEngine
        self.find_in_text_enabled: bool = False
        self.find_in_text_files_max_size_bytes: int = 0

    def __load_rules(self, config: ConfigParser) -> None:
        """Load Finder Rules."""
        rules_sections: List[str] = [item for item in config.sections() if 'FINDER.RULE.' in item]

        # Process Each Rule
        for sec in rules_sections:

            cf_proxy: SectionProxy = config[sec]

            # Get Basic Setting
            rule_spec: Dict = {
                    'id': sec,
                    'instance': None,
                    'notifier': cf_proxy.get('notifier', fallback='').split(','),
                    'exporter': cf_proxy.get('exporter', fallback='').split(','),
                    'type': cf_proxy['type'],
                    }

            # Get Specific Setting
            if cf_proxy['type'] == 'regex':
                rule_spec['instance'] = RegexFinder(config=config[sec])
            elif cf_proxy['type'] == 'all':
                rule_spec['instance'] = AllMessagesFinder(config=config[sec])

            # Normalize Notifier Setting
            rule_spec['notifier'] = list(
                filter(lambda item: item != '', rule_spec['notifier']),
            )
            if len(rule_spec['notifier']) == 0:
                rule_spec['notifier'] = None

            # Normalize Exporter Setting
            rule_spec['exporter'] = list(
                filter(lambda item: item != '', rule_spec['exporter']),
            )
            if len(rule_spec['exporter']) == 0:
                rule_spec['exporter'] = None

            self.rules.append(rule_spec)

    def configure(self, config: ConfigParser, notification_engine: NotifierEngine, exporter_engine: ExporterEngine) -> None:
        """Configure Finder."""
        finder_config_proxy: Optional[SectionProxy] = config['FINDER'] if config.has_section('FINDER') else None

        if finder_config_proxy:

            # Get Basic Props
            self.is_finder_enabled = finder_config_proxy.get('enabled', fallback='false') == 'true'
            self.find_in_text_enabled = finder_config_proxy.get('find_in_text_files_enabled', fallback='false') == 'true'
            self.find_in_text_files_max_size_bytes = int(finder_config_proxy.get('find_in_text_files_max_size_bytes', fallback='10000000'))

            # Load all Rules
            self.__load_rules(config=config)

        else:
            self.find_in_text_enabled = False

        # Set Notification Engine
        self.notification_engine = notification_engine

        # Set Exportation Engine
        self.exporter_engine = exporter_engine

    async def run(self, entity: Optional[FinderNotificationMessageEntity], source: str) -> None:
        """Execute the Finder with Raw Text.

        :param entity: Facade Object
        :param source: Source Account/Phone Number
        :return:
        """
        if not self.is_finder_enabled or not entity:
            return

        cached_file_content: str = ''

        for rule in self.rules:

            # Resolve Finder
            finder: BaseFinder = rule['instance']

            # Find in Raw Text Content
            is_found_on_content: bool = await finder.find(raw_text=entity.raw_text)
            is_found_on_text_downloaded_file: bool = False

            # Find into Downloaded File (If Applicable)
            if not is_found_on_content and self.find_in_text_enabled and rule['type'] != 'all':
                is_found_on_text_downloaded_file = await self.__find_in_text_files(
                    entity=entity,
                    finder=finder,
                    file_content=cached_file_content,
                )

            if is_found_on_content or is_found_on_text_downloaded_file:

                # Update found_on Flag
                entity.found_on = 'MESSAGE' if is_found_on_content else f'FILE\n{entity.downloaded_media_info.disk_file_path}'  # type: ignore

                # Run the Notification Engine
                await self.notification_engine.run(
                    notifiers=rule['notifier'],
                    entity=entity,
                    rule_id=rule['id'],
                    source=source,
                    )

                # Run the Data Export Engine
                if rule['exporter']:
                    await self.exporter_engine.run(
                        exporters=rule['exporter'],
                        entity=entity,
                        rule_id=rule['id'],
                    )

    async def __find_in_text_files(self, entity: FinderNotificationMessageEntity, finder: BaseFinder, file_content: str) -> bool:
        """Try to Run the Finder Engine into the Downloaded Text File."""
        if not entity.downloaded_media_info or not entity.downloaded_media_info.allow_search_in_text_file():
            return False

        # Check if File Exists
        file_exists: bool = await aiofiles.os.path.exists(entity.downloaded_media_info.disk_file_path)
        if not file_exists:
            return False

        # Check Max Size
        max_size_exceeded: bool = entity.downloaded_media_info.size_bytes > self.find_in_text_files_max_size_bytes
        if max_size_exceeded:
            return False

        # Open and Read the File
        if file_content == '':
            async with aiofiles.open(entity.downloaded_media_info.disk_file_path, 'rb') as f:
                file_bytes = await f.read()
                file_content = file_bytes.decode('UTF-8')
                await f.close()

        # Run Finder
        return await finder.find(raw_text=file_content)
