"""Telegram Group Scrapper."""

import base64
import json
import logging
import os
import pathlib
from configparser import ConfigParser
from time import sleep
from typing import Dict, List, Optional, Tuple

import telethon.tl.types
from telethon import TelegramClient
from telethon.errors import ChatAdminRequiredError
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import ChatPhoto, InputPeerEmpty, Message, MessageService, PeerUser
from telethon.tl.types.messages import Dialogs

from TEx.core.base_module import BaseModule
from TEx.core.temp_file import TempFileHandler
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMessageDatabaseManager, \
    TelegramUserDatabaseManager

logger = logging.getLogger()


class TelegramGroupScrapper(BaseModule):
    """List all Groups on Telegram Account."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        if not args['load_groups']:
            logger.info('\t\tModule is Not Enabled...')
            return

        # Check Data Dict
        if 'groups' not in data:
            data['groups'] = {}

        if 'members' not in data:
            data['members'] = {}

        # Get Client
        client: TelegramClient = data['telegram_client']

        # Get all Chats
        chats: List = await self.load_groups(
            client=client
            )

        # Get Only the Groups
        for chat in chats:

            logger.info(f'\t\tProcessing "{chat.title} ({chat.id})" Members and Group Profile Picture')

            values: Dict = {
                'id': chat.id,
                'constructor_id': chat.CONSTRUCTOR_ID,
                'access_hash': str(chat.access_hash),
                'fake': chat.fake,
                'gigagroup': chat.gigagroup,
                'has_geo': chat.has_geo,
                'participants_count': chat.participants_count,
                'restricted': chat.restricted,
                'scam': chat.scam,
                'group_username': chat.username,
                'verified': chat.verified,
                'title': chat.title,
                'source': args['target_phone_number']
                }

            # Get Photo - TODO: Separate in Method
            if chat.photo is not None and isinstance(chat.photo, ChatPhoto):
                values['photo_id'] = chat.photo.photo_id
                photo_name, photo_base64 = await self.get_profile_pic_b64(
                    client=client,
                    channel=chat,
                    data_path=args['data_path'],
                    force_reload=args['refresh_profile_photos']
                    )

                values['photo_base64'] = photo_base64
                values['photo_name'] = photo_name
            else:
                values['photo_id'] = None
                values['photo_base64'] = None
                values['photo_name'] = None

            # Get Members - TODO: Separate in Method
            members = await self.get_members(
                client=client,
                channel=chat
                )

            # Sync with DB
            TelegramUserDatabaseManager.insert_or_update_batch(members)

            # Add Group to DB
            TelegramGroupDatabaseManager.insert_or_update(values)

    async def load_groups(self, client: TelegramClient) -> List[telethon.tl.types.Channel]:
        """Load all Groups from Telegram."""
        logger.info("\t\tEnumerating Groups")

        # DownLoad Groups
        result: Dialogs = await client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=20000,
            hash=0
            ))

        return [chat for chat in result.chats if isinstance(chat, telethon.tl.types.Channel)]

    async def get_members(self, client: TelegramClient, channel: telethon.tl.types.Channel) -> List[Dict]:
        """Download Telegram Group Members."""
        h_result: List = []

        try:

            # Iterate over the Participants
            async for member in client.iter_participants(channel):

                # Build Model
                values: Dict = {
                    'id': member.id,
                    'is_bot': member.bot,
                    'is_fake': member.fake,
                    'is_self': member.is_self,
                    'is_scam': member.scam,
                    'is_verified': member.verified,
                    'first_name': member.first_name,
                    'last_name': member.last_name,
                    'username': member.username,
                    'phone_number': member.phone,
                    'photo_id': None,  # Reserved for Future Version
                    'photo_base64': None,  # Reserved for Future Version
                    'photo_name': None  # Reserved for Future Version
                    }

                # Return
                h_result.append(values)

        except ChatAdminRequiredError:
            logger.info('\t\t\t...Unable to Download Chat Participants due Permission Restrictions...')

        return h_result

    async def get_profile_pic_b64(self, client: TelegramClient, channel: telethon.tl.types.Channel, data_path: str, force_reload: bool = False) -> Tuple[str, str]:
        """
        Download the Profile Picture and Returns as Base64 Image.

        :param client:
        :param channel:
        :param force_reload:
        :return: File Name and File Base64 Content
        """
        target_path: str = f'{data_path}/profile_pic/{channel.id}.jpg'
        temp_file: str = f'profile_pic/{channel.id}.bin'

        # Check Temporary Folder
        if not force_reload and TempFileHandler.file_exist(temp_file):
            temp_data: Dict = json.loads(TempFileHandler.read_file_text(temp_file))

            return temp_data['path'], temp_data['content']

        # Download Photo
        generated_path: str = await client.download_profile_photo(
            entity=channel,
            file=target_path,
            download_big=True
            )

        # Get the Base64
        base_64_content: str = ''
        with open(generated_path, 'rb') as file:
            base_64_content = base64.b64encode(file.read()).decode()
            file.close()

        # Remove File
        os.remove(generated_path)

        # Write Temporary Data
        TempFileHandler.write_file_text(
            path=temp_file,
            content=json.dumps({
                'path': pathlib.Path(generated_path).name,
                'content': base_64_content
                }),
            validate_seconds=604800
            )

        return pathlib.Path(generated_path).name, base_64_content


class TelegramGroupMessageScrapper(BaseModule):
    """Download all Messages from Telegram Groups."""

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        # Get Client
        client: TelegramClient = data['telegram_client']

        if not args['download_messages']:
            logger.info('\t\tModule is Not Enabled...')
            return

        # Check Data Dict
        if 'groups' not in data:
            return

        # Process Single Groups
        for group_id, group_data in data['groups'].items():
            await self.download_messages(
                group_id=group_id,
                client=client,
                group_name=group_data['title']
                )

    async def download_messages(self, group_id: int, group_name: str, client: TelegramClient) -> None:
        """Download all Messages from a Single Group."""
        # Main Download Loop
        while True:

            # Loop Control
            records: int = 0

            # Get the Latest OffSet from Group
            last_offset: Optional[int] = TelegramMessageDatabaseManager.get_max_id_from_group(group_id=group_id)

            # Log
            logger.info(f'\t\tDownload Messages from "{group_name}" > Last Offset: {last_offset}')

            # Wait to Prevent Telegram Flood Detection
            sleep(1)

            # Get all Chats from a Single Group
            # https://docs.telethon.dev/en/latest/modules/client.html#telethon.client.messages.MessageMethods.iter_messages
            async for message in client.iter_messages(
                    group_id,
                    reverse=True,
                    limit=100,
                    min_id=last_offset
                    ):

                # Loop Control
                records += 1

                # Ignore MessageService Messages
                if isinstance(message, MessageService):
                    continue

                # Handle Unknown Types
                if not isinstance(message, Message):
                    logger.debug(f'\t\t{type(message)}')

                values: Dict = {
                    'id': message.id,
                    'group_id': group_id,
                    'date_time': message.date,
                    'message': message.message,
                    'raw': message.raw_text,
                    'to_id': message.to_id.channel_id if message.to_id is not None else None,
                    }

                if message.from_id is not None:
                    if isinstance(message.from_id, PeerUser):
                        values['from_id'] = message.from_id.user_id
                        values['from_type'] = 'User'
                    else:
                        pass

                # Add to DB
                TelegramMessageDatabaseManager.insert(values)

            # Exit Rule
            if records == 0:
                continue
