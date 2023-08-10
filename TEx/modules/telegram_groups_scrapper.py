"""Telegram Group Scrapper."""

import base64
import json
import logging
import os
import pathlib
from configparser import ConfigParser
from typing import Dict, List, Optional, Tuple

import telethon.tl.types
from telethon import TelegramClient
from telethon.errors import ChatAdminRequiredError
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import ChatPhoto, InputPeerEmpty
from telethon.tl.types.messages import Dialogs

from TEx.core.base_module import BaseModule
from TEx.core.mapper.telethon_channel_mapper import TelethonChannelEntiyMapper
from TEx.core.temp_file import TempFileHandler
from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramUserDatabaseManager
from TEx.core.mapper.telethon_user_mapper import TelethonUserEntiyMapper

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

            values: Dict = TelethonChannelEntiyMapper.to_database_dict(
                channel=chat,
                target_phone_numer=config['CONFIGURATION']['phone_number']
                )

            # Get Photo - TODO: Refactory - Separate in Method
            if chat.photo is not None and isinstance(chat.photo, ChatPhoto):
                values['photo_id'] = chat.photo.photo_id
                photo_name, photo_base64 = await self.get_profile_pic_b64(
                    client=client,
                    channel=chat,
                    data_path=config['CONFIGURATION']['data_path'],
                    force_reload=args['refresh_profile_photos']
                    )

                values['photo_base64'] = photo_base64
                values['photo_name'] = photo_name
            else:
                values['photo_id'] = None
                values['photo_base64'] = None
                values['photo_name'] = None

            # Get Members - TODO: Refactory - Separate in Method
            try:
                members = await self.get_members(
                    client=client,
                    channel=chat
                    )

                # Sync with DB
                TelegramUserDatabaseManager.insert_or_update_batch(members)

            except telethon.errors.rpcerrorlist.ChannelPrivateError:
                logger.info('\t\t\t...Unable to Download Chat Participants due Private Chat Restrictions...')
            except ValueError as _ex:
                if 'PeerChannel' in _ex.args[0]:
                    logger.info('\t\t\t...Unable to Download Chat Participants due PerChannel Restrictions...')
                    continue
                raise _ex
            except TypeError as _ex:
                if "'ChannelParticipants' object is not subscriptable" in _ex.args[0]:
                    logger.info('\t\t\t...Unable to Download Chat Participants due ChannelParticipants Restrictions...')
                    continue
                raise _ex

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
                user_dict_data: Dict = TelethonUserEntiyMapper.to_database_dict(member)

                # Return
                h_result.append(user_dict_data)

        except ChatAdminRequiredError:
            logger.info('\t\t\t...Unable to Download Chat Participants due Permission Restrictions...')

        return h_result

    async def get_profile_pic_b64(self, client: TelegramClient, channel: telethon.tl.types.Channel, data_path: str, force_reload: bool = False) -> Tuple[Optional[str], Optional[str]]:
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
        try:
            generated_path: str = await client.download_profile_photo(
                entity=channel,
                file=target_path,
                download_big=True
                )
        except ValueError as ex:
            if 'PeerChannel' in ex.args[0]:
                return None, None

            raise ex

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
