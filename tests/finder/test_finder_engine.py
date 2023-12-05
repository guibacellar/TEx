import asyncio
import datetime
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock
from unittest.mock import ANY, call

from TEx.core.mapper.telethon_message_mapper import TelethonMessageEntityMapper
from TEx.finder.finder_engine import FinderEngine
from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.models.facade.media_handler_facade_entity import MediaHandlingEntity
from tests.modules.common import TestsCommon
from tests.modules.mockups_groups_mockup_data import channel_1_mocked


class FinderEngineTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_run_with_regex_finder(self):
        """Test Run With Regex Finder."""

        # Setup Mock
        notifier_engine_mock = mock.AsyncMock()
        exporter_engine_mock = mock.AsyncMock()

        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime.datetime.utcnow(),
            raw_text="Mocked term3 Raw Text",
            group_name="Group 001",
            group_id=123456,
            from_id="1234",
            to_id=9876,
            reply_to_msg_id=5544,
            message_id=969696,
            is_reply=False,
            downloaded_media_info=None,
            found_on='UTFOUND'
        )

        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        target: FinderEngine = FinderEngine()

        # Execute Discord Notifier Configure Method
        target.configure(
            config=self.config,
            notification_engine=notifier_engine_mock,
            exporter_engine=exporter_engine_mock
        )
        target.notification_engine = notifier_engine_mock

        loop = asyncio.get_event_loop()
        loop.run_until_complete(

            # Invoke Test Target
            target.run(
                entity=message_entity,
                source='+15558987453'
            )
        )

        # Get Expected Entity for the Notification Engine
        expected_entity: FinderNotificationMessageEntity = message_entity.model_copy(deep=True)
        expected_entity.found_on = 'MESSAGE'

        # Check if Webhook was Executed
        target.notification_engine.run.assert_has_awaits([
            call(notifiers=['NOTIFIER.DISCORD.NOT_002'], entity=expected_entity, rule_id='FINDER.RULE.UT_Finder_Demo', source='+15558987453'),
            call(notifiers=['NOTIFIER.DISCORD.NOT_002'], entity=expected_entity, rule_id='FINDER.RULE.UT_Finder_Demo_MultiLine', source='+15558987453'),
            call(notifiers=['NOTIFIER.DISCORD.NOT_002'], entity=expected_entity, rule_id='FINDER.RULE.UT_Finder_Demo_MultiLine_WithLineBreak', source='+15558987453'),
        ])

    def test_run_not_found(self):
        """Test Run With Nothing Find."""

        # Setup Mock
        notifier_engine_mock = mock.AsyncMock()
        exporter_engine_mock = mock.AsyncMock()

        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime.datetime.utcnow(),
            raw_text="Mocked term4 Raw Text",
            group_name="Group 001",
            group_id=123456,
            from_id="1234",
            to_id=9876,
            reply_to_msg_id=5544,
            message_id=969696,
            is_reply=False,
            downloaded_media_info=None,
            found_on='UTFOUND'
        )

        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        target: FinderEngine = FinderEngine()

        # Execute Discord Notifier Configure Method
        target.configure(
            config=self.config,
            notification_engine=notifier_engine_mock,
            exporter_engine=exporter_engine_mock
        )
        target.notification_engine = notifier_engine_mock

        loop = asyncio.get_event_loop()
        loop.run_until_complete(

            # Invoke Test Target
            target.run(
                entity=message_entity,
                source='+15558987453'
            )
        )

        # Check if Webhook was Executed
        target.notification_engine.run.assert_not_called()

    def test_run_with_regex_finder_on_file(self):
        """Test Run With Regex Finder on Downloaded File."""

        # Setup Mock
        notifier_engine_mock = mock.AsyncMock()
        exporter_engine_mock = mock.AsyncMock()

        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime.datetime.utcnow(),
            raw_text="Mocked Raw Text",
            group_name="Group 002",
            group_id=123456,
            from_id="1234",
            to_id=9876,
            reply_to_msg_id=5544,
            message_id=969696,
            is_reply=False,
            downloaded_media_info=MediaHandlingEntity(
                media_id=123,
                file_name='LargeDownloadedFile.txt',
                content_type='text/plain',
                size_bytes=12279,
                disk_file_path='resources/LargeDownloadedFile.txt',
                is_ocr_supported=False,
            ),
            found_on='UTFOUND'
        )

        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        target: FinderEngine = FinderEngine()

        # Execute Discord Notifier Configure Method
        target.configure(
            config=self.config,
            notification_engine=notifier_engine_mock,
            exporter_engine=exporter_engine_mock
        )
        target.notification_engine = notifier_engine_mock

        loop = asyncio.get_event_loop()
        loop.run_until_complete(

            # Invoke Test Target
            target.run(
                entity=message_entity,
                source='+15558987453'
            )
        )

        # Get Expected Entity for the Notification Engine
        expected_entity: FinderNotificationMessageEntity = message_entity.model_copy(deep=True)
        expected_entity.found_on = 'FILE\nresources/LargeDownloadedFile.txt'

        # Check if Webhook was Executed
        target.notification_engine.run.assert_has_awaits([
            call(notifiers=['NOTIFIER.DISCORD.NOT_002'], entity=expected_entity, rule_id='FINDER.RULE.UT_Finder_Demo', source='+15558987453'),
            call(notifiers=['NOTIFIER.DISCORD.NOT_002'], entity=expected_entity, rule_id='FINDER.RULE.UT_Finder_Demo_MultiLine', source='+15558987453'),
            call(notifiers=['NOTIFIER.DISCORD.NOT_002'], entity=expected_entity, rule_id='FINDER.RULE.UT_Finder_Demo_MultiLine_WithLineBreak', source='+15558987453'),
        ])