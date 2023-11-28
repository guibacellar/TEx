import asyncio
import datetime
import os
import pickle
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock
import shutil
import pytz

import pandas as pd

from TEx.exporter.pandas_rolling_exporter import PandasRollingExporter
from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from tests.modules.common import TestsCommon

# TODO: Verify if Keep Last Files Algorithm are Working Properly

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
            config=self.config['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001'],
            source='+15558987453'
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
        self.assertIsNotNone(target.current_df)
        self.assertEqual(
            ['date_time', 'raw_text', 'group_name', 'group_id', 'from_id', 'to_id', 'reply_to_msg_id', 'message_id', 'is_reply', 'found_on'],
            list(target.current_df.columns.values)
            )

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

        # Validate output - Files Generated
        self.ensure_has_files(
            expected_files=[
                'tex_export_15558987453_202311221007.csv',
                'tex_export_15558987453_202311221007_5.csv',
                'tex_export_15558987453_202311221007_6.csv',
                'tex_export_15558987453_202311221007_4.csv',
                'tex_export_15558987453_202311221007_3.csv',
                'tex_export_15558987453_202311221007_2.csv',
                'tex_export_15558987453_202311221007_1.csv',
                'tex_export_15558987453_202311221006.csv',
                'tex_export_15558987453_202311221005.csv'
            ]
        )

        # Validate output - Files Content (Check One File Only)
        self.validate_file_content('tex_export_15558987453_202311221007.csv', 'test_pandas_rolling_exporter_csv_expected_15558987453_202311221007.data')

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

        # Validate output - Files Generated
        self.ensure_has_files(
            expected_files=[
                'tex_export_15558987453_202311221007.xml',
                'tex_export_15558987453_202311221007_5.xml',
                'tex_export_15558987453_202311221007_6.xml',
                'tex_export_15558987453_202311221007_4.xml',
                'tex_export_15558987453_202311221007_3.xml',
                'tex_export_15558987453_202311221007_2.xml',
                'tex_export_15558987453_202311221007_1.xml',
                'tex_export_15558987453_202311221006.xml',
                'tex_export_15558987453_202311221005.xml'
            ]
        )

        # Validate output - Files Content (Check One File Only)
        self.validate_file_content('tex_export_15558987453_202311221007_3.xml', 'test_pandas_rolling_exporter_xml_expected_15558987453_202311221007_3.data')

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

        # Validate output - Files Generated
        self.ensure_has_files(
            expected_files=[
                'tex_export_15558987453_202311221005.json',
                'tex_export_15558987453_202311221006.json',
                'tex_export_15558987453_202311221007.json',
                'tex_export_15558987453_202311221007_1.json',
                'tex_export_15558987453_202311221007_2.json',
                'tex_export_15558987453_202311221007_3.json',
                'tex_export_15558987453_202311221007_4.json',
                'tex_export_15558987453_202311221007_5.json',
                'tex_export_15558987453_202311221007_6.json',
            ]
        )

        # Validate output - Files Content (Check One File Only)
        self.validate_file_content('tex_export_15558987453_202311221005.json', 'test_pandas_rolling_exporter_json_expected_15558987453_202311221005.data')

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

        # Validate output - Files Generated
        self.ensure_has_files(
            expected_files=[
                'tex_export_15558987453_202311221005.bin',
                'tex_export_15558987453_202311221006.bin',
                'tex_export_15558987453_202311221007.bin',
                'tex_export_15558987453_202311221007_1.bin',
                'tex_export_15558987453_202311221007_2.bin',
                'tex_export_15558987453_202311221007_3.bin',
                'tex_export_15558987453_202311221007_4.bin',
                'tex_export_15558987453_202311221007_5.bin',
                'tex_export_15558987453_202311221007_6.bin',
            ]
        )

        # Validate output - Files Content
        readed_generated_dataframe = pd.read_pickle(os.path.join('_data/export', 'tex_export_15558987453_202311221005.bin'))
        self.assertIsNotNone(readed_generated_dataframe)
        self.assertEqual(10, len(readed_generated_dataframe))

        for ix in range(len(readed_generated_dataframe)):
            self.assertEqual(datetime.datetime(2023, 11, 22, 10, 22, tzinfo=pytz.UTC), readed_generated_dataframe.iloc[ix]['date_time'])
            self.assertEqual('Mocked Raw Text', readed_generated_dataframe.iloc[ix]['raw_text'])
            self.assertEqual('Channel 1972142108', readed_generated_dataframe.iloc[ix]['group_name'])
            self.assertEqual(1972142108, readed_generated_dataframe.iloc[ix]['group_id'])
            self.assertEqual(1234, readed_generated_dataframe.iloc[ix]['from_id'])
            self.assertEqual(9876, readed_generated_dataframe.iloc[ix]['to_id'])
            self.assertEqual(5544, readed_generated_dataframe.iloc[ix]['reply_to_msg_id'])
            self.assertEqual(5975883, readed_generated_dataframe.iloc[ix]['message_id'])
            self.assertFalse(readed_generated_dataframe.iloc[ix]['is_reply'])
            self.assertEqual('UT FOUND 6', readed_generated_dataframe.iloc[ix]['found_on'])

    @mock.patch('TEx.exporter.pandas_rolling_exporter.datetime')
    def __execute_main_run(self, target, mocked_date_time):

        # Set Message
        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime.datetime(2023, 11, 22, 10, 22, tzinfo=pytz.UTC),
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
            config=self.config['EXPORTER.ROLLING_PANDAS.TEST_EXPORTER_001'],
            source='+15558987453'
        )

        # Execute the Runner
        loop = asyncio.get_event_loop()

        # Run 10
        for i in range(10):
            loop.run_until_complete(
                target.run(entity=message_entity, rule_id='RULE_UT_01')
            )

        # Force Change Time (+1 Minute) to Rollup the File
        mocked_date_time.now = mock.MagicMock(return_value=datetime.datetime(year=2023, month=11, day=22, hour=10, minute=6, second=40, microsecond=100))
        message_entity.date_time = datetime.datetime(year=2023, month=11, day=22, hour=10, minute=6, second=40, microsecond=100)

        # Run 9 Times
        for i in range(9):
            loop.run_until_complete(
                target.run(entity=message_entity, rule_id='RULE_UT_01')
            )

        # Force Change Time (+1 Minute) to Rollup the File
        mocked_date_time.now = mock.MagicMock(return_value=datetime.datetime(year=2023, month=11, day=22, hour=10, minute=7, second=40, microsecond=101))
        message_entity.date_time = datetime.datetime(year=2023, month=11, day=22, hour=10, minute=7, second=40, microsecond=101)

        # Run 14 Times
        for i in range(14):
            loop.run_until_complete(
                target.run(entity=message_entity, rule_id='RULE_UT_01')
            )

        # Repeat 6 Times to Ensure the Code that handle multi files with same pattern to run
        for i in range(6):
            # Force Flush
            target._PandasRollingExporter__flush()

            # Run Again to Call the Multiple File with same name Handling
            loop.run_until_complete(
                target.run(entity=message_entity, rule_id='RULE_UT_01')
            )

        # Shutdown Engine
        target.shutdown()

    def get_file_content(self, file_path):

        with open(file_path, 'r') as file:
            return file.readlines()

    def validate_file_content(self, generated_file, expected_content_file_path):

        generated_file_content = self.get_file_content(os.path.join('_data/export', generated_file))
        reference_file_content = self.get_file_content(os.path.join('resources/expected_generated_file_content', expected_content_file_path))

        # Check Line Count
        self.assertEqual(len(generated_file_content), len(reference_file_content), 'Expected File Content has Different Line Number from Generated File')

        for ix in range(len(reference_file_content)):
            self.assertEqual(generated_file_content[ix], reference_file_content[ix], f'Expected Line not Match the Generated File at Index {ix}')

    def ensure_has_files(self, expected_files):
        # Validate output - Files Generated
        for name in expected_files:
            self.assertTrue(os.path.exists(os.path.join('_data/export', name)))
