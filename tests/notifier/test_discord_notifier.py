import asyncio
import datetime
import unittest
from configparser import ConfigParser
from typing import Dict
from unittest import mock

from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.models.facade.media_handler_facade_entity import MediaHandlingEntity
from TEx.models.facade.signal_notification_model import SignalNotificationEntityModel
from TEx.notifier.discord_notifier import DiscordNotifier
from tests.modules.common import TestsCommon
from tests.modules.mockups_groups_mockup_data import channel_1_mocked


class DiscordNotifierTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = ConfigParser()
        self.config.read('../../config.ini')

    def test_run_no_duplication(self):
        """Test Run Method First Time - No Duplication Detection."""

        # Setup Mock
        discord_webhook_mock = mock.AsyncMock()
        discord_webhook_mock.add_embed = mock.MagicMock()

        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime.datetime(2023, 10, 1, 9, 58, 22),
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

        target: DiscordNotifier = DiscordNotifier()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        with mock.patch('TEx.notifier.discord_notifier.AsyncDiscordWebhook', return_value=discord_webhook_mock):
            # Execute Discord Notifier Configure Method
            target.configure(
                config=self.config['NOTIFIER.DISCORD.NOT_001'],
                url='url.domain/path'
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

        # Check is Embed was Added into Webhook
        discord_webhook_mock.add_embed.assert_called_once()
        call_arg = discord_webhook_mock.add_embed.call_args[0][0]

        self.assertEqual(call_arg.title, '**Channel 1972142108** (1972142108)')
        self.assertEqual(call_arg.description, 'Mocked Raw Text')

        self.assertEqual(len(call_arg.fields), 7)
        self.assertEqual(call_arg.fields[0], {'inline': True, 'name': 'Source', 'value': '+15558987453'})
        self.assertEqual(call_arg.fields[1], {'inline': True, 'name': 'Rule', 'value': 'RULE_UT_01'})
        self.assertEqual(call_arg.fields[2], {'inline': False, 'name': 'Message ID', 'value': '5975883'})
        self.assertEqual(call_arg.fields[3], {'inline': True, 'name': 'Group Name', 'value': 'Channel 1972142108'})
        self.assertEqual(call_arg.fields[4], {'inline': True, 'name': 'Group ID', 'value': '1972142108'})
        self.assertEqual(call_arg.fields[6], {'inline': False, 'name': 'Tag', 'value': 'de33f5dda9c686c64d23b8aec2eebfc7'})

        # Check if Webhook was Executed
        discord_webhook_mock.execute.assert_awaited_once()

    def test_run_duplication_control(self):
        """Test Run Method First Time - With Duplication Detection."""

        # Setup Mock
        discord_webhook_mock = mock.AsyncMock()
        discord_webhook_mock.add_embed = mock.MagicMock()

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
        )

        target: DiscordNotifier = DiscordNotifier()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        with mock.patch('TEx.notifier.discord_notifier.AsyncDiscordWebhook', return_value=discord_webhook_mock):
            # Execute Discord Notifier Configure Method
            target.configure(
                config=self.config['NOTIFIER.DISCORD.NOT_001'],
                url='url.domain/path'
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

            loop.run_until_complete(

                # Invoke Test Target Again
                target.run(
                    entity=message_entity,
                    rule_id='RULE_UT_01',
                    source='+15558987453'
                )
            )

        # Check is Embed was Added into Webhook Exact 1 Time
        discord_webhook_mock.add_embed.assert_called_once()

        # Check if Webhook was Executed Exact 1 Time
        discord_webhook_mock.execute.assert_awaited_once()

    def test_run_with_downloaded_media_image(self):
        """Test Run Method With Downloaded Media as Image."""

        # Setup Mock
        discord_webhook_mock = mock.AsyncMock()
        discord_webhook_mock.add_embed = mock.MagicMock()
        discord_webhook_mock.add_file = mock.MagicMock()

        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime.datetime(2023, 10, 1, 9, 58, 22),
            raw_text="Mocked Raw Text",
            group_name="Channel 1972142108",
            group_id=1972142108,
            from_id="1234",
            to_id=9876,
            reply_to_msg_id=5544,
            message_id=5975883,
            is_reply=False,
            downloaded_media_info=MediaHandlingEntity(
                media_id=555,
                file_name='122761750_387013276008970_8208112669996447119_n.jpg',
                content_type='image/png',
                size_bytes=1520,
                disk_file_path='resources/122761750_387013276008970_8208112669996447119_n.jpg',
                is_ocr_supported=True
            ),
        )

        target: DiscordNotifier = DiscordNotifier()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        with mock.patch('TEx.notifier.discord_notifier.AsyncDiscordWebhook', return_value=discord_webhook_mock):
            # Execute Discord Notifier Configure Method
            target.configure(
                config=self.config['NOTIFIER.DISCORD.NOT_001'],
                url='url.domain/path'
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

        # Check is Embed was Added into Webhook
        discord_webhook_mock.add_embed.assert_called_once()
        discord_webhook_mock.add_file.assert_called_once()
        embed_call_arg = discord_webhook_mock.add_embed.call_args[0][0]
        add_file_arg = discord_webhook_mock.add_file.call_args[1]

        self.assertEqual(embed_call_arg.title, '**Channel 1972142108** (1972142108)')
        self.assertEqual(embed_call_arg.description, 'Mocked Raw Text')

        self.assertEqual(len(embed_call_arg.fields), 7)
        self.assertEqual(embed_call_arg.fields[0], {'inline': True, 'name': 'Source', 'value': '+15558987453'})
        self.assertEqual(embed_call_arg.fields[1], {'inline': True, 'name': 'Rule', 'value': 'RULE_UT_01'})
        self.assertEqual(embed_call_arg.fields[2], {'inline': False, 'name': 'Message ID', 'value': '5975883'})
        self.assertEqual(embed_call_arg.fields[3], {'inline': True, 'name': 'Group Name', 'value': 'Channel 1972142108'})
        self.assertEqual(embed_call_arg.fields[4], {'inline': True, 'name': 'Group ID', 'value': '1972142108'})
        self.assertEqual(embed_call_arg.fields[6], {'inline': False, 'name': 'Tag', 'value': 'de33f5dda9c686c64d23b8aec2eebfc7'})

        self.assertEqual(embed_call_arg.image['url'], 'attachment://122761750_387013276008970_8208112669996447119_n.jpg')

        self.assertEqual(add_file_arg['filename'], '122761750_387013276008970_8208112669996447119_n.jpg')
        self.assertIsNotNone(add_file_arg['file'])

        # Check if Webhook was Executed
        discord_webhook_mock.execute.assert_awaited_once()

    def test_run_with_downloaded_media_video(self):
        """Test Run Method With Downloaded Media as Video."""

        # Setup Mock
        discord_webhook_mock = mock.AsyncMock()
        discord_webhook_mock.add_embed = mock.MagicMock()
        discord_webhook_mock.add_file = mock.MagicMock()

        message_entity: FinderNotificationMessageEntity = FinderNotificationMessageEntity(
            date_time=datetime.datetime(2023, 10, 1, 9, 58, 22),
            raw_text="Mocked Raw Text",
            group_name="Channel 1972142108",
            group_id=1972142108,
            from_id="1234",
            to_id=9876,
            reply_to_msg_id=5544,
            message_id=5975883,
            is_reply=False,
            downloaded_media_info=MediaHandlingEntity(
                media_id=555,
                file_name='unknow.mp4',
                content_type='video/mp4',
                size_bytes=1520,
                disk_file_path='resources/unknow.mp4',
                is_ocr_supported=False
            ),
        )

        target: DiscordNotifier = DiscordNotifier()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        with mock.patch('TEx.notifier.discord_notifier.AsyncDiscordWebhook', return_value=discord_webhook_mock):
            # Execute Discord Notifier Configure Method
            target.configure(
                config=self.config['NOTIFIER.DISCORD.NOT_001'],
                url='url.domain/path'
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

        # Check is Embed was Added into Webhook
        discord_webhook_mock.add_embed.assert_called_once()
        discord_webhook_mock.add_file.assert_called_once()
        embed_call_arg = discord_webhook_mock.add_embed.call_args[0][0]
        add_file_arg = discord_webhook_mock.add_file.call_args[1]

        self.assertEqual(embed_call_arg.title, '**Channel 1972142108** (1972142108)')
        self.assertEqual(embed_call_arg.description, 'Mocked Raw Text')

        self.assertEqual(len(embed_call_arg.fields), 7)
        self.assertEqual(embed_call_arg.fields[0], {'inline': True, 'name': 'Source', 'value': '+15558987453'})
        self.assertEqual(embed_call_arg.fields[1], {'inline': True, 'name': 'Rule', 'value': 'RULE_UT_01'})
        self.assertEqual(embed_call_arg.fields[2], {'inline': False, 'name': 'Message ID', 'value': '5975883'})
        self.assertEqual(embed_call_arg.fields[3], {'inline': True, 'name': 'Group Name', 'value': 'Channel 1972142108'})
        self.assertEqual(embed_call_arg.fields[4], {'inline': True, 'name': 'Group ID', 'value': '1972142108'})
        self.assertEqual(embed_call_arg.fields[6], {'inline': False, 'name': 'Tag', 'value': 'de33f5dda9c686c64d23b8aec2eebfc7'})

        self.assertEqual(embed_call_arg.video['url'], 'attachment://unknow.mp4')

        self.assertEqual(add_file_arg['filename'], 'unknow.mp4')
        self.assertIsNotNone(add_file_arg['file'])

        # Check if Webhook was Executed
        discord_webhook_mock.execute.assert_awaited_once()

    def test_run_with_signal(self):
        """Test Run Method With Signal Input."""

        # Setup Mock
        discord_webhook_mock = mock.AsyncMock()
        discord_webhook_mock.add_embed = mock.MagicMock()
        discord_webhook_mock.add_file = mock.MagicMock()

        message_entity: SignalNotificationEntityModel = SignalNotificationEntityModel(
            signal='INITIALIZATION',
            date_time=datetime.datetime(2023, 10, 1, 9, 58, 22),
            content='Signal Content'
        )

        target: DiscordNotifier = DiscordNotifier()
        args: Dict = {
            'config': 'unittest_configfile.config'
        }
        data: Dict = {}
        TestsCommon.execute_basic_pipeline_steps_for_initialization(config=self.config, args=args, data=data)

        with mock.patch('TEx.notifier.discord_notifier.AsyncDiscordWebhook', return_value=discord_webhook_mock):
            # Execute Discord Notifier Configure Method
            target.configure(
                config=self.config['NOTIFIER.DISCORD.NOT_001'],
                url='url.domain/path'
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

        # Check is Embed was Added into Webhook
        discord_webhook_mock.add_embed.assert_called_once()
        embed_call_arg = discord_webhook_mock.add_embed.call_args[0][0]

        self.assertEqual(embed_call_arg.title, 'INITIALIZATION')
        self.assertEqual(embed_call_arg.description, 'Signal Content')

        self.assertEqual(len(embed_call_arg.fields), 2)
        self.assertEqual(embed_call_arg.fields[0], {'inline': True, 'name': 'Source', 'value': '+15558987453'})

        # Check if Webhook was Executed
        discord_webhook_mock.execute.assert_awaited_once()
