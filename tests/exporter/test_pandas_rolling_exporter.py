import asyncio
import datetime
import os
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock
import shutil
import pytz

from TEx.exporter.pandas_rolling_exporter import PandasRollingExporter
from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from tests.modules.common import TestsCommon


class PandasRollingExporterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # Remove all Files from Exporter Folder
        if os.path.exists('_data/export'):
            shutil.rmtree('_data/export')

        os.mkdir('_data/export')

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

    def test_run_as_csv(self):
        """Test Run Method Exporting as CSV."""

        # Setup Mock
        target: PandasRollingExporter = PandasRollingExporter()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Execute Class
        self.__execute_main_run(target)

        # TODO: Validate output

    def test_run_as_xml(self):
        """Test Run Method Exporting as XML."""

        # Setup Mock
        target: PandasRollingExporter = PandasRollingExporter()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)
        self.config['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001']['output_format'] = 'xml'

        # Execute Class
        self.__execute_main_run(target)

        # TODO: Validate output

    def test_run_as_json(self):
        """Test Run Method Exporting as JSON."""

        # Setup Mock
        target: PandasRollingExporter = PandasRollingExporter()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)
        self.config['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001']['output_format'] = 'json'

        # Execute Class
        self.__execute_main_run(target)

        # TODO: Validate output

    def test_run_as_pickle(self):
        """Test Run Method Exporting as Pickle File."""

        # Setup Mock
        target: PandasRollingExporter = PandasRollingExporter()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)
        self.config['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001']['output_format'] = 'pickle'

        # Execute Class
        self.__execute_main_run(target)

        # TODO: Validate output

    @mock.patch('TEx.exporter.pandas_rolling_exporter.datetime')
    def __execute_main_run(self, target, mocked_date_time):

        # Set Message
        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime.datetime(2023, 11, 22, 58, 22, tzinfo=pytz.UTC),
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
        mocked_date_time.now = mock.MagicMock(return_value=datetime.datetime(year=2023, month=11, day=22, hour=10, minute=5, second=33, microsecond=99))
        target.configure(
            config=self.config['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001']
        )

        # Execute the Runner
        loop = asyncio.get_event_loop()

        # Run 10
        for i in range(10):
            loop.run_until_complete(
                target.run(entity=message_entity, rule_id='RULE_UT_01', source='+15558987453')
            )

        # Force Change Time (+1 Minute) to Rollup the File
        mocked_date_time.now = mock.MagicMock(return_value=datetime.datetime(year=2023, month=11, day=22, hour=10, minute=6, second=40, microsecond=100))
        message_entity.date_time = datetime.datetime(year=2023, month=11, day=22, hour=10, minute=6, second=40, microsecond=100)

        # Run 9 Times
        for i in range(9):
            loop.run_until_complete(
                target.run(entity=message_entity, rule_id='RULE_UT_01', source='+15558987453')
            )

        # Force Change Time (+1 Minute) to Rollup the File
        mocked_date_time.now = mock.MagicMock(return_value=datetime.datetime(year=2023, month=11, day=22, hour=10, minute=7, second=40, microsecond=101))
        message_entity.date_time = datetime.datetime(year=2023, month=11, day=22, hour=10, minute=7, second=40, microsecond=101)

        # Run 14 Times
        for i in range(14):
            loop.run_until_complete(
                target.run(entity=message_entity, rule_id='RULE_UT_01', source='+15558987453')
            )

        target.shutdown()
