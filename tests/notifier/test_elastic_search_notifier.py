import asyncio
import datetime
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock

import pytz

from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.models.facade.media_handler_facade_entity import MediaHandlingEntity
from TEx.notifier.elastic_search_notifier import ElasticSearchNotifier
from tests.modules.common import TestsCommon


class ElasticSearchNotifierTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_configure_with_hosts(self):
        """Test configure method with hosts."""
        # Setup Mock
        elastic_search_api_mock = mock.MagicMock()

        target: ElasticSearchNotifier = ElasticSearchNotifier()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Change Config Map
        self.config['NOTIFIER.ELASTIC_SEARCH.UT_01'].clear()
        self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']['address'] = 'http://localhost:1,http://localhost:2'
        self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']['api_key'] = 'MyApiKey003'
        self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']['verify_ssl_cert'] = 'False'
        self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']['index_name'] = 'UT_IndexName_004'
        self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']['pipeline_name'] = 'UT_PipelineName_005'

        # Set Message
        with mock.patch('TEx.notifier.elastic_search_notifier.AsyncElasticsearch', return_value=elastic_search_api_mock) as patched_ctor:
            # Execute Discord Notifier Configure Method
            target.configure(
                config=self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']
            )

            # Check Call Args
            call_arg = patched_ctor.call_args[1]
            self.assertEqual('http://localhost:1', call_arg['hosts'][0])
            self.assertEqual('http://localhost:2', call_arg['hosts'][1])
            self.assertEqual('MyApiKey003', call_arg['api_key'])
            self.assertEqual(False, call_arg['verify_certs'])
            self.assertIsNone(call_arg['cloud_id'])

    def test_configure_with_cloud_id(self):
        """Test configure method with Cloud ID Info."""
        # Setup Mock
        elastic_search_api_mock = mock.MagicMock()

        target: ElasticSearchNotifier = ElasticSearchNotifier()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Change Config Map
        self.config['NOTIFIER.ELASTIC_SEARCH.UT_01'].clear()
        self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']['cloud_id'] = 'deployment-name:dXMtZWFzdDQuZ2Nw'
        self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']['index_name'] = 'UT_IndexName_007'
        self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']['pipeline_name'] = 'UT_PipelineName_008'

        # Set Message
        with mock.patch('TEx.notifier.elastic_search_notifier.AsyncElasticsearch',
                        return_value=elastic_search_api_mock) as patched_ctor:
            # Execute Discord Notifier Configure Method
            target.configure(
                config=self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']
            )

            # Check Call Args
            call_arg = patched_ctor.call_args[1]
            self.assertEqual('deployment-name:dXMtZWFzdDQuZ2Nw', call_arg['cloud_id'])
            self.assertEqual(True, call_arg['verify_certs'])
            self.assertIsNone(call_arg['hosts'])
            self.assertIsNone(call_arg['api_key'])

    def test_run_without_downloaded_file(self):
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

        # Set Message
        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime.datetime(2023, 10, 1, 9, 58, 22, tzinfo=pytz.UTC),
            raw_text="Mocked Raw Text",
            group_name="Channel 1972142108",
            group_id=1972142108,
            from_id="1234",
            to_id=9876,
            reply_to_msg_id=5544,
            message_id=5975883,
            is_reply=False,
            downloaded_media_info=None,
        )

        with mock.patch('TEx.notifier.elastic_search_notifier.AsyncElasticsearch', return_value=elastic_search_api_mock):
            # Execute Discord Notifier Configure Method
            target.configure(
                config=self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']
            )

            loop = asyncio.get_event_loop()
            loop.run_until_complete(

                # Invoke Test Target
                target.run(
                    entity=message_entity,
                    rule_id='RULE_UT_01',
                    source='+15558987453'
                )
            )

        # Check .index call
        elastic_search_api_mock.index.assert_called_once()
        call_arg = elastic_search_api_mock.index.call_args[1]

        self.assertEqual(call_arg['index'], 'test_index_name')
        self.assertEqual(call_arg['pipeline'], 'test_pipeline_name')
        self.assertEqual(call_arg['id'], '1972142108_5975883')

        submited_document = call_arg['document']
        expected_document = {
            'time': datetime.datetime(2023, 10, 1, 9, 58, 22, tzinfo=pytz.UTC),
            'source': '+15558987453',
            'rule': 'RULE_UT_01',
            'raw': 'Mocked Raw Text',
            'group_name': 'Channel 1972142108',
            'group_id': 1972142108,
            'from_id': 1234,
            'to_id': 9876,
            'reply_to_msg_id': 5544,
            'message_id': 5975883,
            'is_reply': False,
            'has_media': False,
            'media_mime_type': None,
            'media_size': None
        }

        self.assertEqual(submited_document, expected_document)

    def test_run_with_downloaded_file(self):
        """Test Run Method With Message File Attachment."""

        # Setup Mock
        elastic_search_api_mock = mock.AsyncMock()
        elastic_search_api_mock.index = mock.AsyncMock()

        target: ElasticSearchNotifier = ElasticSearchNotifier()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Set Message
        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime.datetime(2023, 10, 1, 9, 58, 22, tzinfo=pytz.UTC),
            raw_text="Mocked Raw Text 2",
            group_name="Channel 1972142101",
            group_id=1972142108,
            from_id="1234",
            to_id=9876,
            reply_to_msg_id=5544,
            message_id=5975883,
            is_reply=False,
            downloaded_media_info=MediaHandlingEntity(
                media_id=99,
                file_name='utfile.pdf',
                content_type='application/pdf',
                size_bytes=5858,
                disk_file_path='/folder/file.png',
                is_ocr_supported=True
            ),
        )

        with mock.patch('TEx.notifier.elastic_search_notifier.AsyncElasticsearch', return_value=elastic_search_api_mock):
            # Execute Discord Notifier Configure Method
            target.configure(
                config=self.config['NOTIFIER.ELASTIC_SEARCH.UT_01']
            )

            loop = asyncio.get_event_loop()
            loop.run_until_complete(

                # Invoke Test Target
                target.run(
                    entity=message_entity,
                    rule_id='RULE_UT_01',
                    source='+15558987453'
                )
            )

        # Check .index call
        elastic_search_api_mock.index.assert_called_once()
        call_arg = elastic_search_api_mock.index.call_args[1]

        self.assertEqual(call_arg['index'], 'test_index_name')
        self.assertEqual(call_arg['pipeline'], 'test_pipeline_name')
        self.assertEqual(call_arg['id'], '1972142108_5975883')

        submited_document = call_arg['document']
        expected_document = {
            'time': datetime.datetime(2023, 10, 1, 9, 58, 22, tzinfo=pytz.UTC),
            'source': '+15558987453',
            'rule': 'RULE_UT_01',
            'raw': 'Mocked Raw Text 2',
            'group_name': 'Channel 1972142101',
            'group_id': 1972142108,
            'from_id': 1234,
            'to_id': 9876,
            'reply_to_msg_id': 5544,
            'message_id': 5975883,
            'is_reply': False,
            'has_media': True,
            'media_mime_type': 'application/pdf',
            'media_size': 5858
        }

        self.assertEqual(submited_document, expected_document)
