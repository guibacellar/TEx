import asyncio
import datetime
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock

from TEx.notifier.discord_notifier import DiscordNotifier
from tests.modules.common import TestsCommon
from tests.modules.mockups_groups_mockup_data import channel_1_mocked


class DiscordNotifierTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_run_no_duplication(self):
        """Test Run Method First Time - No Duplication Detection."""

        # Setup Mock
        discord_webhook_mock = mock.AsyncMock()
        discord_webhook_mock.add_embed = mock.MagicMock()

        target_message = mock.MagicMock()
        target_message.raw_text = "Mocked Raw Text"
        target_message.id = 5975883
        target_message.data = datetime.datetime(2023, 10, 1, 9, 58, 22)
        target_message.chat = channel_1_mocked

        target: DiscordNotifier = DiscordNotifier()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        with mock.patch('TEx.notifier.discord_notifier.DiscordWebhook', return_value=discord_webhook_mock):
            loop = self._extracted_from_test_run_duplication_control_23(
                target, target_message
            )
        # Check is Embed was Added into Webhook
        discord_webhook_mock.add_embed.assert_called_once()
        call_arg = discord_webhook_mock.add_embed.call_args[0][0]

        self.assertEqual(call_arg.title, '**Channel 1972142108** (1972142108)')
        self.assertEqual(call_arg.description, 'Mocked Raw Text')

        self.assertEqual(len(call_arg.fields), 6)
        self.assertEqual(call_arg.fields[0], {'inline': False, 'name': 'Rule', 'value': 'RULE_UT_01'})
        self.assertEqual(call_arg.fields[1], {'inline': False, 'name': 'Message ID', 'value': '5975883'})
        self.assertEqual(call_arg.fields[2], {'inline': True, 'name': 'Group Name', 'value': 'Channel 1972142108'})
        self.assertEqual(call_arg.fields[3], {'inline': True, 'name': 'Group ID', 'value': 1972142108})
        self.assertEqual(call_arg.fields[5],
                         {'inline': False, 'name': 'Tag', 'value': 'de33f5dda9c686c64d23b8aec2eebfc7'})

        # Check if Webhook was Executed
        discord_webhook_mock.execute.assert_called_once()

    def test_run_duplication_control(self):
        """Test Run Method First Time - With Duplication Detection."""

        # Setup Mock
        discord_webhook_mock = mock.AsyncMock()
        discord_webhook_mock.add_embed = mock.MagicMock()

        target_message = mock.MagicMock()
        target_message.raw_text = "Mocked Raw Text 2"
        target_message.id = 5975883
        target_message.data = datetime.datetime(2023, 10, 1, 9, 58, 22)
        target_message.chat = channel_1_mocked

        target: DiscordNotifier = DiscordNotifier()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        with mock.patch('TEx.notifier.discord_notifier.DiscordWebhook', return_value=discord_webhook_mock):
            loop = self._extracted_from_test_run_duplication_control_23(
                target, target_message
            )
            loop.run_until_complete(

                # Invoke Test Target Again
                target.run(
                    message=target_message,
                    rule_id='RULE_UT_01'
                )
            )

        # Check is Embed was Added into Webhook Exact 1 Time
        discord_webhook_mock.add_embed.assert_called_once()

        # Check if Webhook was Executed Exact 1 Time
        discord_webhook_mock.execute.assert_called_once()

    # TODO Rename this here and in `test_run_no_duplication` and `test_run_duplication_control`
    def _extracted_from_test_run_duplication_control_23(self, target, target_message):
        target.configure(
            config=self.config['NOTIFIER.DISCORD.NOT_001'], url='url.domain/path'
        )
        result = asyncio.get_event_loop()
        result.run_until_complete(
            target.run(message=target_message, rule_id='RULE_UT_01')
        )
        return result
