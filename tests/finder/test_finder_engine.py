import asyncio
import datetime
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock
from unittest.mock import ANY, call

from TEx.finder.finder_engine import FinderEngine
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

        target_message = mock.MagicMock()
        target_message.raw_text = "Mocked term3 Raw Text"

        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        with mock.patch('TEx.finder.finder_engine.NotifierEngine', return_value=notifier_engine_mock):
            target: FinderEngine = FinderEngine()

            # Execute Discord Notifier Configure Method
            target.configure(
                config=self.config
            )
            target.notification_engine = notifier_engine_mock

            loop = asyncio.get_event_loop()
            loop.run_until_complete(

                # Invoke Test Target
                target.run(
                    message=target_message
                )
            )

        # Check if Webhook was Executed
        target.notification_engine.run.assert_awaited_once_with(
            notifiers=['NOTIFIER.DISCORD.NOT_002'],
            message=target_message,
            rule_id='FINDER.RULE.UT_Finder_Demo'
        )
