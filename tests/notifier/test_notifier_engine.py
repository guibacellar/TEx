import asyncio
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock
from unittest.mock import call

from TEx.notifier.notifier_engine import NotifierEngine
from tests.modules.common import TestsCommon
from tests.modules.mockups_groups_mockup_data import base_messages_mockup_data


class NotifierEngineTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_run(self):
        """Test Run Method with Telegram Server Connection."""

        # Setup Mock
        discord_notifier_mockup = mock.AsyncMock()
        discord_notifier_mockup.run = mock.AsyncMock()

        target: NotifierEngine = NotifierEngine()
        args: Dict = {
            'export_text': True,
            'config': 'unittest_configfile.config',
            'report_folder': '_report',
            'group_id': '2',
            'order_desc': True,
            'filter': 'Message',
            'limit_days': 30,
            'regex': '(.*http://.*),(.*https://.*)'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        with mock.patch('TEx.notifier.notifier_engine.DiscordNotifier', return_value=discord_notifier_mockup):
            target.configure(config=self.config)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                target.run(
                    notifiers=['NOTIFIER.DISCORD.NOT_001', 'NOTIFIER.DISCORD.NOT_002'],
                    message=base_messages_mockup_data[0],
                    rule_id='RULE_UT_01'
                )
            )

            discord_notifier_mockup.run.assert_has_awaits([
                call(message=base_messages_mockup_data[0], rule_id='RULE_UT_01'),
                call(message=base_messages_mockup_data[0], rule_id='RULE_UT_01'),
            ])
