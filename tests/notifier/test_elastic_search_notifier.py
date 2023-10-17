import asyncio
import datetime
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock

from telethon.tl.types import Message, MessageFwdHeader, PeerChannel, PeerUser

from TEx.notifier.discord_notifier import DiscordNotifier
from TEx.notifier.elastic_search_notifier import ElasticSearchNotifier
from tests.modules.common import TestsCommon
from tests.modules.mockups_groups_mockup_data import base_groups_mockup_data, base_messages_mockup_data, \
    channel_1_mocked


class ElasticSearchNotifierTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_run_without_file(self):
        """Test Run Method Without Message File Attachment."""

        # Setup Mock
        elastic_search_api_mock = mock.AsyncMock()
        elastic_search_api_mock.index = mock.AsyncMock()

        target: ElasticSearchNotifier = ElasticSearchNotifier()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Set Mock Message
        origin_mock_message = base_messages_mockup_data[1]
        mocked_message = mock.MagicMock(spec=origin_mock_message)
        for attr_name in origin_mock_message.__dict__:
            setattr(mocked_message, attr_name, getattr(origin_mock_message, attr_name))
        mocked_message.chat = channel_1_mocked

        with mock.patch('TEx.notifier.elastic_search_notifier.AsyncElasticsearch', return_value=elastic_search_api_mock):
            # Execute Discord Notifier Configure Method
            target.configure(
                config=self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']
            )

            loop = asyncio.get_event_loop()
            loop.run_until_complete(

                # Invoke Test Target
                target.run(
                    message=mocked_message,
                    rule_id='RULE_UT_01',
                    source='+15558987453'
                )
            )

        # Check .index call
        elastic_search_api_mock.index.assert_called_once()
        call_arg = elastic_search_api_mock.index.call_args[1]

        self.assertEqual(call_arg['index'], 'test_index_name')
        self.assertEqual(call_arg['pipeline'], 'test_pipeline_name')
        self.assertEqual(call_arg['id'], '1972142108_183017')

        submited_document = call_arg['document']
