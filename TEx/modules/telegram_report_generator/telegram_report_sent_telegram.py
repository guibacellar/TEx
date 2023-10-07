"""Telegram Report Generator."""
from __future__ import annotations

import asyncio
import datetime
import logging
import os
import zipfile
from configparser import ConfigParser
from os.path import basename
from typing import Dict, cast

import pytz
from telethon import TelegramClient

from TEx.core.base_module import BaseModule

logger = logging.getLogger('TelegramExplorer')


class TelegramReportSentViaTelegram(BaseModule):
    """Sent the Report to a Telegram user."""

    __USERS_RESOLUTION_CACHE: Dict = {}

    async def can_activate(self, config: ConfigParser, args: Dict, data: Dict) -> bool:
        """
        Abstract Method for Module Activation Function..

        :return:
        """
        return cast(bool, args['sent_report_telegram'])

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not await self.can_activate(config, args, data):
            logger.debug('\t\tModule is Not Enabled...')
            return

        # Check Report and Assets Folder
        report_root_folder: str = args['report_folder']

        # Create Report File Name
        attach_name: str = args['attachment_name'].replace('@@now@@', datetime.datetime.strftime(datetime.datetime.now(tz=pytz.UTC), '%y%m%d_%H%M%S')) + '.zip'
        report_filename: str = os.path.join(report_root_folder, attach_name)
        logger.info(f'\t\t\tTarget Report Filename: {report_filename}')

        # Create a Zip File
        logger.info('\t\t\tGenerating Report ZIP File')
        with zipfile.ZipFile(report_filename, 'w', compresslevel=9, compression=zipfile.ZIP_DEFLATED) as zip_obj:
            # Iterate over all the files in directory
            for folder_name, _subfolders, filenames in os.walk(report_root_folder):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)

                    if file_path == report_filename:
                        continue

                    zip_obj.write(file_path, os.path.join(basename(folder_name), filename))

        # Sent via Telegram
        client: TelegramClient = data['telegram_client']
        receiver = await client.get_input_entity(args['destination_username'])

        # Sent Message
        logger.info('\t\t\tSending Message')
        await client.send_message(
            receiver,
            args['title'].replace(
                '@@now@@',
                datetime.datetime.strftime(datetime.datetime.now(tz=pytz.UTC), '%y-%m-%d %H:%M:%S'),
                ).replace('\\n', '\n'),
            )
        await asyncio.sleep(1)
        # Sent the Report
        await client.send_file(receiver, f'{report_root_folder}/{attach_name}')

        # Remove Report File
        os.remove(report_filename)
