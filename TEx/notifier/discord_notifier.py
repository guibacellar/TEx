"""Discord Notifier."""
from __future__ import annotations

import os
from configparser import SectionProxy
from typing import Union

import aiofiles
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed

from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
from TEx.models.facade.signal_notification_model import SignalNotificationEntityModel
from TEx.notifier.notifier_base import BaseNotifier


class DiscordNotifier(BaseNotifier):
    """Basic Discord Notifier."""

    def __init__(self) -> None:
        """Initialize Discord Notifier."""
        super().__init__()
        self.url: str = ''

    def configure(self, url: str, config: SectionProxy) -> None:
        """Configure the Notifier."""
        self.url = url
        self.configure_base(config=config)

    async def run(self, entity: Union[FinderNotificationMessageEntity, SignalNotificationEntityModel], rule_id: str, source: str) -> None:
        """Run Discord Notifier."""
        # Run the Notification Process
        webhook = AsyncDiscordWebhook(  # type: ignore
            url=self.url,
            rate_limit_retry=True,
            timeout=self.timeout_seconds,
        )

        embed: DiscordEmbed
        if isinstance(entity, FinderNotificationMessageEntity):
            is_duplicated, duplication_tag = self.check_is_duplicated(message=entity.raw_text)
            if is_duplicated:
                return

            embed = await self.__get_finder_notification_embed(
                entity=entity,
                rule_id=rule_id,
                source=source,
                duplication_tag=duplication_tag,
            )

            # Handle Attachments
            await self.__handle_attachment(
                entity=entity,
                webhook=webhook,
                embed=embed,
            )

        else:
            embed = await self.__get_signal_notification_embed(
                entity=entity,
                source=source,
            )

        webhook.add_embed(embed)
        await webhook.execute(remove_embeds=True)

    async def __handle_attachment(self, entity: FinderNotificationMessageEntity, webhook: AsyncDiscordWebhook, embed: DiscordEmbed) -> None:
        """Handle the Attachment Upload."""
        if not entity.downloaded_media_info or not self.media_attachments_enabled:
            return

        # Check Max Size
        if entity.downloaded_media_info.size_bytes > self.media_attachments_max_size_bytes:
            return

        # Upload File
        if os.path.exists(entity.downloaded_media_info.disk_file_path):

            # Open and Upload
            async with aiofiles.open(entity.downloaded_media_info.disk_file_path, 'rb') as f:
                webhook.add_file(file=await f.read(), filename=f'{entity.downloaded_media_info.file_name}')
                await f.close()

            # Add on Embed
            if entity.downloaded_media_info.is_image():
                embed.set_image(url=f'attachment://{entity.downloaded_media_info.file_name}')

            elif entity.downloaded_media_info.is_video():
                embed.set_video(url=f'attachment://{entity.downloaded_media_info.file_name}')

    async def __get_signal_notification_embed(self, entity: SignalNotificationEntityModel, source: str) -> DiscordEmbed:
        """Return the Embed Object for Signals."""
        embed = DiscordEmbed(
            title=entity.signal,
            description=entity.content,
            )

        embed.add_embed_field(name='Source', value=source, inline=True)
        embed.add_embed_field(name='Message Date', value=str(entity.date_time), inline=True)

        return embed

    async def __get_finder_notification_embed(self, entity: FinderNotificationMessageEntity, rule_id: str, source: str, duplication_tag: str) -> DiscordEmbed:
        """Return the Embed Object for Notification."""
        # Build Title
        title: str = ''
        if entity.group_name and entity.group_id:
            title = f'**{entity.group_name}** ({entity.group_id})'
        elif entity.group_name:
            title = f'**{entity.group_name}**'
        elif entity.group_id:
            title = f'**{entity.group_id}**'

        embed = DiscordEmbed(
            title=title,
            description=entity.raw_text,
            )

        embed.add_embed_field(name='Source', value=source, inline=True)
        embed.add_embed_field(name='Rule', value=rule_id, inline=True)

        if entity.message_id:
            embed.add_embed_field(name='Message ID', value=str(entity.message_id), inline=False)

        if entity.group_id:
            embed.add_embed_field(name='Group Name', value=entity.group_name if entity.group_name else '', inline=True)
            embed.add_embed_field(name='Group ID', value=str(entity.group_id), inline=True)

        embed.add_embed_field(name='Found On', value=entity.found_on, inline=False)
        embed.add_embed_field(name='Message Date', value=str(entity.date_time), inline=False)
        embed.add_embed_field(name='Tag', value=duplication_tag, inline=False)

        return embed
