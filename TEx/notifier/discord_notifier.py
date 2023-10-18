"""Discord Notifier."""
from configparser import SectionProxy

from discord_webhook import DiscordEmbed, DiscordWebhook

from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity
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

    async def run(self, entity: FinderNotificationMessageEntity, rule_id: str, source: str) -> None:
        """Run Discord Notifier."""
        # Check and Update Deduplication Control
        is_duplicated, duplication_tag = self.check_is_duplicated(message=entity.raw_text)
        if is_duplicated:
            return

        # Run the Notification Process.
        webhook = DiscordWebhook(
            url=self.url,
            rate_limit_retry=True,
            )

        embed = DiscordEmbed(
            title=f'**{entity.group_name}** ({entity.group_id})',
            description=entity.raw_text,
            )

        embed.add_embed_field(name='Source', value=source, inline=True)
        embed.add_embed_field(name='Rule', value=rule_id, inline=True)
        embed.add_embed_field(name='Message ID', value=str(entity.message_id), inline=False)
        embed.add_embed_field(name='Group Name', value=entity.group_name if entity.group_name else '', inline=True)
        embed.add_embed_field(name='Group ID', value=str(entity.group_id), inline=True)
        embed.add_embed_field(name='Message Date', value=str(entity.date_time), inline=False)
        embed.add_embed_field(name='Tag', value=duplication_tag, inline=False)

        # add embed object to webhook
        webhook.add_embed(embed)
        webhook.execute()
