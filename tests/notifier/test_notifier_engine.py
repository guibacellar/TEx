import asyncio
import unittest
from configparser import ConfigParser
from datetime import datetime
from typing import Dict
from unittest import mock
from unittest.mock import call

from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
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

        elastic_notifier_mockup = mock.AsyncMock()
        elastic_notifier_mockup.run = mock.AsyncMock()

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

        # Set Message
        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime(2023, 10, 1, 9, 58, 22),
            raw_text="Mocked Raw Text",
            group_name="Channel 1972142108",
            group_id=1972142108,
            from_id="1234",
            to_id=9876,
            reply_to_msg_id=5544,
            message_id=55,
            is_reply=False,
            downloaded_media_info=None,
            found_on='UT FOUND 7'
        )

        with mock.patch('TEx.notifier.notifier_engine.DiscordNotifier', return_value=discord_notifier_mockup):
            with mock.patch('TEx.notifier.notifier_engine.ElasticSearchNotifier', return_value=elastic_notifier_mockup):
                target.configure(config=self.config)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(
                    target.run(
                        notifiers=['NOTIFIER.DISCORD.NOT_001', 'NOTIFIER.DISCORD.NOT_002', 'NOTIFIER.ELASTIC_SEARCH.UT_01'],
                        entity=message_entity,
                        rule_id='RULE_UT_01',
                        source='+15558987453'
                    )
                )

                discord_notifier_mockup.run.assert_has_awaits([
                    call(entity=message_entity, rule_id='RULE_UT_01', source='+15558987453'),
                    call(entity=message_entity, rule_id='RULE_UT_01', source='+15558987453')
                ])

                elastic_notifier_mockup.run.assert_has_awaits([
                    call(entity=message_entity, rule_id='RULE_UT_01', source='+15558987453')
                ])
