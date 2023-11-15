import asyncio
import datetime
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock

import pytz

from TEx.exporter.pandas_rolling_exporter import PandasRollingExporter
from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.models.facade.media_handler_facade_entity import MediaHandlingEntity
from TEx.models.facade.signal_notification_model import SignalNotificationEntityModel
from TEx.notifier.elastic_search_notifier import ElasticSearchNotifier
from tests.modules.common import TestsCommon


class PandasRollingExporterTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_configure(self):
        """Test configure method."""
        # Setup Mock
        elastic_search_api_mock = mock.MagicMock()

        target: PandasRollingExporter = PandasRollingExporter()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Execute Configure Method
        target.configure(
            config=self.config['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001']
            )

        # Check Configurations
        self.assertEqual(1, target.rolling_every_minutes)
        self.assertEqual(
            'date_time,raw_text,group_name,group_id,from_id,to_id,reply_to_msg_id,message_id,is_reply,found_on'.split(','),
            target.fields
        )
        self.assertTrue(target.use_header)
        self.assertEqual('csv', target.export_format)

        # Check DataFrame
        # TODO: Pending

    def test_run(self):
        """Test Run Method."""

        # Setup Mock
        target: PandasRollingExporter = PandasRollingExporter()
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
            found_on='UT FOUND 6'
        )

        # Execute Configure Method
        target.configure(
            config=self.config['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001']
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
