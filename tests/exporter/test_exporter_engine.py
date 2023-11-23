import asyncio
import datetime
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock

import pytz

from TEx.exporter.exporter_engine import ExporterEngine
from TEx.exporter.pandas_rolling_exporter import PandasRollingExporter
from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.models.facade.media_handler_facade_entity import MediaHandlingEntity
from TEx.models.facade.signal_notification_model import SignalNotificationEntityModel
from TEx.notifier.elastic_search_notifier import ElasticSearchNotifier
from tests.modules.common import TestsCommon


class ExporterEngineTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_configure(self):
        """Test configure method."""
        # Setup Mock
        target: ExporterEngine = ExporterEngine()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Execute Configure Method
        target.configure(config=self.config)

        # Check Configurations
        self.assertEqual(1, len(target.exporters))
        self.assertEqual('EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001', list(target.exporters.keys())[0])
        self.assertTrue(
            isinstance(target.exporters['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001']['instance'], PandasRollingExporter)
        )

    @mock.patch('TEx.exporter.exporter_engine.PandasRollingExporter')
    def test_run(self, patched_exporter):
        """Test run method."""
        # Setup Mock
        target: ExporterEngine = ExporterEngine()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Execute Configure Method
        target.configure(config=self.config)

        # Configure the Mock
        patched_exporter.run = mock.AsyncMock()
        target.exporters['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001']['instance'] = patched_exporter

        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime.datetime(2023, 10, 1, 9, 58, 22),
            raw_text="Mocked Raw Text 2",
            group_name="Channel 1972142108",
            group_id=1972142108,
            from_id="1234",
            to_id=9876,
            reply_to_msg_id=5544,
            message_id=5975883,
            is_reply=False,
            downloaded_media_info=None,
            found_on='UT FOUND'
        )

        loop = asyncio.get_event_loop()
        loop.run_until_complete(

            # Invoke Test Target
            target.run(
                exporters=['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001'],
                entity=message_entity,
                rule_id='RULE_UT_01',
                source='+15558987453'
            )
        )

        patched_exporter.run.assert_awaited_once_with(
            entity=message_entity,
            rule_id='RULE_UT_01',
            source='+15558987453'
        )
