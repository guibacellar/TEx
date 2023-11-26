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
                rule_id='RULE_UT_01'
            )
        )

        patched_exporter.run.assert_awaited_once_with(
            entity=message_entity,
            rule_id='RULE_UT_01'
        )

    @mock.patch('TEx.exporter.exporter_engine.PandasRollingExporter')
    def test_run_with_exporter_error(self, patched_exporter):
        """Test run method when an Exporter Throws an Error."""
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
        patched_exporter.run = mock.AsyncMock(side_effect=Exception())
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

        with self.assertLogs() as captured:

            loop = asyncio.get_event_loop()
            loop.run_until_complete(

                # Invoke Test Target
                target.run(
                    exporters=['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001'],
                    entity=message_entity,
                    rule_id='RULE_UT_01'
                )
            )

            # Check if Code Handle the Error
            self.assertEqual(1, len(captured.records))
            self.assertEqual('Unable to Export Data',captured.records[0].message)

    def test_run_without_exporters(self):
        """Test run method without any exporter. Expected has no Errors"""
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
        target.exporters = []

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
                exporters=[],
                entity=message_entity,
                rule_id='RULE_UT_01'
            )
        )

    @mock.patch('TEx.exporter.exporter_engine.PandasRollingExporter')
    def test_shutdown(self, patched_exporter):
        """Test the shutdown method."""
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
        patched_exporter.shutdown = mock.MagicMock()
        target.exporters['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001']['instance'] = patched_exporter

        loop = asyncio.get_event_loop()
        loop.run_until_complete(

            # Invoke Test Target
            target.shutdown()
        )

        patched_exporter.shutdown.assert_called_once()

    def test_shutdown_without_exporters(self):
        """Test the shutdown method without Any Exporter. Expected has no Errors."""
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
        target.exporters = []

        loop = asyncio.get_event_loop()
        loop.run_until_complete(

            # Invoke Test Target
            target.shutdown()
        )

    @mock.patch('TEx.exporter.exporter_engine.PandasRollingExporter')
    def test_shutdown_with_error(self, patched_exporter):
        """Test the shutdown method when one exporter raises an Exception. Expected has no Failtures and only a Log"""
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
        patched_exporter.shutdown = mock.MagicMock(side_effect=Exception())
        target.exporters['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001']['instance'] = patched_exporter

        with self.assertLogs() as captured:

            loop = asyncio.get_event_loop()
            loop.run_until_complete(

                # Invoke Test Target
                target.shutdown()
            )

            # Check if Code Handles the Error
            self.assertEqual(1, len(captured.records))
            self.assertEqual('Unable to Shutdown the "EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001" Exporter Gracefully. Data may be lost.', captured.records[0].message)

