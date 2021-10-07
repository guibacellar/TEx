"""Telegram Report Generator."""
import base64
import datetime
import logging

from configparser import ConfigParser
from typing import Dict, List, Optional, cast

import pytz

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

from TEx import DirectoryManagerUtils
from TEx.core.base_module import BaseModule
from TEx.database.TelegramGroupDatabase import (
    TelegramGroupDatabaseManager,
    TelegramMediaDatabaseManager,
    TelegramMessageDatabaseManager,
    TelegramUserDatabaseManager
    )

from TEx.models.database.telegram_db_model import (
    TelegramGroupOrmEntity,
    TelegramMediaOrmEntity,
    TelegramMessageOrmEntity,
    TelegramUserOrmEntity
    )

logger = logging.getLogger()


class TelegramReportGenerator(BaseModule):
    """Generate Report from Telegram Groups."""

    __USERS_RESOLUTION_CACHE: Dict = {}

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not args['report']:
            logger.info('\t\tModule is Not Enabled...')
            return

        # Check Report and Assets Folder
        report_root_folder: str = args['report_folder']
        assets_root_folder: str = f'{report_root_folder}/assets/'
        DirectoryManagerUtils.ensure_dir_struct(report_root_folder)
        DirectoryManagerUtils.ensure_dir_struct(assets_root_folder)

        # Get Report Template
        env = Environment(
            loader=FileSystemLoader("report_templates"),
            autoescape=select_autoescape()
            )
        template: Template = env.get_template("default_template.html")

        # Load Groups from DB
        groups: List[TelegramGroupOrmEntity] = TelegramGroupDatabaseManager.get_all_by_phone_number(
            args['target_phone_number'])
        logger.info(f'\t\tFound {len(groups)} Groups')

        # Process Each Group
        for group in groups:
            logger.info(f'\t\tProcessing "{group.title}"')
            await self.draw_report(args, assets_root_folder, group, report_root_folder, template)

    async def draw_report(self, args: Dict, assets_root_folder: str, group: TelegramGroupOrmEntity, report_root_folder: str, template: Template) -> None:
        """Process the Report for a Single Group Chat."""
        # Download All Messages
        logger.info('\t\t\tRetrieving Messages')
        messages: List[TelegramMessageOrmEntity] = TelegramMessageDatabaseManager.get_all_messages_from_group(
            group_id=group.id,
            order_by_desc=args['order_desc']
            )

        # Filter Messages
        logger.info('\t\t\tFiltering')
        filter_words: Optional[List[str]] = args['filter'].upper().split(',') if args['filter'] else None
        messages = self.filter_messages(messages=messages, filter_words=filter_words)

        # Limits Configuration
        limit_days: int = int(args['limit_days'])
        limit_seconds: int = limit_days * 24 * 60 * 60
        logger.info('\t\t\tProcessing Messages')

        # Generate Object to Render
        render_messages: List = await self.process_messages(
            messages=messages,
            limit_seconds=limit_seconds,
            assets_root_folder=assets_root_folder
            )

        logger.info('\t\t\tRendering')
        with open(f'{report_root_folder}/result_{group.id}.html', 'wb') as file:
            output = template.render(
                groupname=group.title,
                messages=render_messages
                )
            file.write(output.encode('utf-8'))
            file.flush()
            file.close()

    async def process_messages(self, messages: List[TelegramMessageOrmEntity], limit_seconds: int, assets_root_folder: str) -> List[TelegramMediaOrmEntity]:
        """Process Group Messages."""
        h_result: List = []

        # Process Each Message
        for message in messages:

            # Check Message Limit
            delta_seconds: datetime.timedelta = datetime.datetime.now(tz=pytz.utc) - pytz.utc.localize(message.date_time)
            if delta_seconds.total_seconds() > limit_seconds:
                continue

            # Get the From Message User
            from_user: Optional[TelegramUserOrmEntity] = self.get_user(message.from_id)

            # Check if Append the Message on Previous Message OR Creates a New One
            is_user_bot: bool = from_user is not None and not from_user.is_bot
            not_has_media = message.media_id is None
            is_same_user: bool = len(h_result) > 0 and h_result[-1]['from_id'] == message.from_id and h_result[-1]['to_id'] == message.to_id

            if is_user_bot and is_same_user and not_has_media:

                # Attach to Previous Message
                h_result[-1]['message'] += '\r\n' + message.message

            else:

                # Process new Message
                entry: Dict = {
                    'id': message.id,
                    'date_time': message.date_time,
                    'from_id': message.from_id,
                    'to_id': message.to_id,
                    'message': message.message,
                    'to_from_information': self.render_to_from_message_info(message=message, from_user=from_user)
                    }

                # Process Media
                entry.update(await self.get_media(message=message, assets_root_folder=assets_root_folder))

                h_result.append(entry)

        return h_result

    async def get_media(self, message: TelegramMessageOrmEntity, assets_root_folder: str) -> Dict:
        """Download Media and Return the Metadata."""
        media_file_name: Optional[str] = None
        media_mime_type: Optional[str] = None
        media_geo: Optional[str] = None
        media_title: Optional[str] = None

        # Check if Have Media
        if message.media_id:

            # Get Media from DB
            media: Optional[TelegramMediaOrmEntity] = TelegramMediaDatabaseManager.get_by_id(message.media_id)

            if media:
                if media.mime_type == 'application/vnd.geo':
                    media_geo = media.title.replace('|', ',')
                else:

                    # Save into assets folder
                    with open(f'{assets_root_folder}{media.file_name}', 'wb') as file:
                        if not media.b64_content:
                            file.write(''.encode())
                        else:
                            file.write(base64.b64decode(media.b64_content))
                        file.flush()
                        file.close()

                    media_file_name = f'assets/{media.file_name}'
                    media_title = media.title

                media_mime_type = media.mime_type

                return {
                    'media_filename': media_file_name,
                    'media_mime_type': media_mime_type,
                    'media_geo': media_geo,
                    'media_title': media_title,
                    'media_is_image': media_mime_type and ('image/' in media_mime_type or media_mime_type == 'photo')
                    }

        return {
            'media_filename': None,
            'media_mime_type': None,
            'media_geo': None,
            'media_title': None,
            'media_is_image': None
            }

    def render_to_from_message_info(self, message: TelegramMessageOrmEntity, from_user: Optional[TelegramUserOrmEntity]) -> str:
        """Build and Return the TO/FROM Information for Message."""
        # Get Users
        to_user: Optional[TelegramUserOrmEntity] = self.get_user(message.to_id)

        to_from_information: str = ''
        if from_user:
            to_from_information += f'- ({from_user.username}) {from_user.first_name if from_user.first_name else ""} {from_user.last_name if from_user.last_name else ""}' if from_user else ''
        if to_user:
            to_from_information += f' in reply to ({to_user.username}) {to_user.first_name if to_user.first_name else ""} {to_user.last_name if to_user.last_name else ""}' if to_user else ''

        return to_from_information

    def get_user(self, user_id: int) -> Optional[TelegramUserOrmEntity]:
        """Return the User from DB Resolution."""
        if user_id not in TelegramReportGenerator.__USERS_RESOLUTION_CACHE:
            TelegramReportGenerator.__USERS_RESOLUTION_CACHE.update(
                {user_id: TelegramUserDatabaseManager.get_by_id(user_id)}
                )

        return cast(Optional[TelegramUserOrmEntity], TelegramReportGenerator.__USERS_RESOLUTION_CACHE[user_id])

    def filter_messages(self, messages: List[TelegramMessageOrmEntity], filter_words: Optional[List[str]]) -> List[TelegramMessageOrmEntity]:
        """Filter Messages."""
        if not filter_words or len(filter_words) == 0:
            return messages

        h_result: List[TelegramMessageOrmEntity] = []

        for message in messages:
            for word in filter_words:
                if word in message.raw.upper():
                    h_result.append(message)
                    break

        return h_result
