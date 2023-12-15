import asyncio
import datetime
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock
from unittest.mock import ANY, call

import pytz

from TEx.models.facade.signal_notification_model import SignalNotificationEntityModel
from TEx.notifier.signals_engine import SignalsEngine, SignalsEngineFactory
from tests.modules.common import TestsCommon


class SignalsEngineFactoryTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    @mock.patch('TEx.notifier.signals_engine.NotifierEngine')
    def test_get_instance(self, mocked_signal_engine):
        """Test get_instance Method with Success."""
        args: Dict = {
            'config': 'unittest_configfile.config',
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        h_result: SignalsEngine = SignalsEngineFactory.get_instance(
            config=self.config,
            notification_engine=mocked_signal_engine,
            source='+1234567809'
        )

        # Check Results
        self.assertEqual(mocked_signal_engine, h_result.notification_engine)
        self.assertTrue(h_result.signal_entity.enabled)
        self.assertEqual(2, h_result.signal_entity.keep_alive_interval)
        self.assertEqual(['NOTIFIER.DISCORD.NOT_001'], h_result.signal_entity.notifiers['KEEP-ALIVE'])
        self.assertEqual(['NOTIFIER.ELASTIC_SEARCH.UT_01'], h_result.signal_entity.notifiers['INITIALIZATION'])
        self.assertEqual(['NOTIFIER.DISCORD.NOT_001', 'NOTIFIER.ELASTIC_SEARCH.UT_01'], h_result.signal_entity.notifiers['SHUTDOWN'])
        self.assertEqual(['NOTIFIER.ELASTIC_SEARCH.UT_01', 'NOTIFIER.DISCORD.NOT_001'], h_result.signal_entity.notifiers['NEW-GROUP'])

    @mock.patch('TEx.notifier.signals_engine.NotifierEngine')
    def test_get_instance_without_signals_on_config_file(self, mocked_signal_engine):
        """Test get_instance Method with Success When Have no SIGNALS section on Config File."""
        args: Dict = {
            'config': 'unittest_configfile.config',
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        self.config.remove_section('SIGNALS')

        h_result: SignalsEngine = SignalsEngineFactory.get_instance(
            config=self.config,
            notification_engine=mocked_signal_engine,
            source='+1234567809'
        )

        # Check Results
        self.assertEqual(mocked_signal_engine, h_result.notification_engine)
        self.assertFalse(h_result.signal_entity.enabled)
        self.assertEqual(300, h_result.signal_entity.keep_alive_interval)
        self.assertEqual([], h_result.signal_entity.notifiers['KEEP-ALIVE'])
        self.assertEqual([], h_result.signal_entity.notifiers['INITIALIZATION'])
        self.assertEqual([], h_result.signal_entity.notifiers['SHUTDOWN'])
        self.assertEqual([], h_result.signal_entity.notifiers['NEW-GROUP'])


class SignalsEngineTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    @mock.patch('TEx.notifier.signals_engine.NotifierEngine')
    def test_keep_alive(self, mocked_signal_engine):
        """Test keep_alive method."""
        args: Dict = {
            'config': 'unittest_configfile.config',
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Configure Mock
        mocked_signal_engine.run = mock.AsyncMock()

        target: SignalsEngine = SignalsEngineFactory.get_instance(
            config=self.config,
            notification_engine=mocked_signal_engine,
            source='+1234567809'
        )
        for i in range(10):
            target.inc_messages_sent()

        # Invoke Test Target
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            target.keep_alive()
        )

        # Check Results
        mocked_signal_engine.run.assert_has_awaits([
            call(
                notifiers=['NOTIFIER.DISCORD.NOT_001'],
                entity=ANY,
                rule_id='SIGNALS',
                source='+1234567809'
            )
        ])

        # Check Entity Used
        self.__check_result_entity(
            mocked_signal_engine=mocked_signal_engine,
            signal='KEEP-ALIVE',
            message='Messages Processed in Period: 10'
        )

        # Check the Messages Sent Counter Reset
        self.assertEqual(0, target.messages_sent)

    @mock.patch('TEx.notifier.signals_engine.NotifierEngine')
    def test_shutdown(self, mocked_signal_engine):
        """Test shutdown Method."""
        args: Dict = {
            'config': 'unittest_configfile.config',
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Configure Mock
        mocked_signal_engine.run = mock.AsyncMock()

        target: SignalsEngine = SignalsEngineFactory.get_instance(
            config=self.config,
            notification_engine=mocked_signal_engine,
            source='+1234567802'
        )
        for i in range(9):
            target.inc_messages_sent()

        # Invoke Test Target
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            target.shutdown()
        )

        # Check Results
        mocked_signal_engine.run.assert_has_awaits([
            call(
                notifiers=['NOTIFIER.DISCORD.NOT_001', 'NOTIFIER.ELASTIC_SEARCH.UT_01'],
                entity=ANY,
                rule_id='SIGNALS',
                source='+1234567802'
            )
        ])

        # Check Entity Used
        self.__check_result_entity(
            mocked_signal_engine=mocked_signal_engine,
            signal='SHUTDOWN',
            message='Last Messages Processed in Period: 9'
        )

    @mock.patch('TEx.notifier.signals_engine.NotifierEngine')
    def test_init(self, mocked_signal_engine):
        """Test init Method."""
        args: Dict = {
            'config': 'unittest_configfile.config',
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Configure Mock
        mocked_signal_engine.run = mock.AsyncMock()

        target: SignalsEngine = SignalsEngineFactory.get_instance(
            config=self.config,
            notification_engine=mocked_signal_engine,
            source='+1234567801'
        )

        # Invoke Test Target
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            target.init()
        )

        # Check Results
        mocked_signal_engine.run.assert_has_awaits([
            call(
                notifiers=['NOTIFIER.ELASTIC_SEARCH.UT_01'],
                entity=ANY,
                rule_id='SIGNALS',
                source='+1234567801'
            )
        ])

        # Check Entity Used
        self.__check_result_entity(
            mocked_signal_engine=mocked_signal_engine,
            signal='INITIALIZATION',
            message=''
        )

    @mock.patch('TEx.notifier.signals_engine.NotifierEngine')
    def test_new_group(self, mocked_signal_engine):
        """Test new_group Method."""
        args: Dict = {
            'config': 'unittest_configfile.config',
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        # Configure Mock
        mocked_signal_engine.run = mock.AsyncMock()

        target: SignalsEngine = SignalsEngineFactory.get_instance(
            config=self.config,
            notification_engine=mocked_signal_engine,
            source='+12345678451'
        )

        # Invoke Test Target
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            target.new_group(
                group_id='9988',
                group_title='UT Group Title'
            )
        )

        # Check Results
        mocked_signal_engine.run.assert_has_awaits([
            call(
                notifiers=['NOTIFIER.ELASTIC_SEARCH.UT_01', 'NOTIFIER.DISCORD.NOT_001'],
                entity=ANY,
                rule_id='SIGNALS',
                source='+12345678451'
            )
        ])

        # Check Entity Used
        self.__check_result_entity(
            mocked_signal_engine=mocked_signal_engine,
            signal='NEW-GROUP',
            message='ID: 9988 | Title: "UT Group Title"'
        )

    def __check_result_entity(self, mocked_signal_engine, signal: str, message: str):

        # Check Entity Used
        entity: SignalNotificationEntityModel = mocked_signal_engine.run.mock_calls[0][2]['entity']
        self.assertEqual(signal, entity.signal)
        self.assertEqual(message, entity.content)

        time_delta_seconds: datetime.timedelta = datetime.datetime.now(tz=pytz.UTC) - entity.date_time
        self.assertTrue(time_delta_seconds.seconds <= 1)
