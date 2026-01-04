import discord
import logfire
from injector import inject

from src.system.domain.value.messenger import MessengerName
from src.system.domain.value.nickname import (
    NicknameChangelogBefore,
    NicknameChangelogAfter,
)
from src.system.domain.value.user import UserID
from src.system.ui.discord.config import DiscordConfigIf
from src.system.ui.discord.error_handler import send_error_embed
from src.system.usecase.nickname.dto import RecordNicknameChangeRequest
from src.system.usecase.nickname.interface import RecordNicknameChangeUsecaseIf


class DiscordBot(discord.Client):
    """Discord bot client that handles member update events."""

    _MESSENGER_NAME = "discord"

    @inject
    def __init__(
        self,
        config: DiscordConfigIf,
        record_nickname_change_usecase: RecordNicknameChangeUsecaseIf,
    ) -> None:
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(intents=intents)

        self._config = config
        self._record_nickname_change_usecase = record_nickname_change_usecase

    @logfire.instrument(span_name="DiscordBot.on_member_update()")
    async def on_member_update(
        self, before: discord.Member, after: discord.Member
    ) -> None:
        """Handle member update events.

        Records nickname changes to the database.
        """
        if before.nick == after.nick:
            return

        request = RecordNicknameChangeRequest(
            messenger_name=MessengerName(self._MESSENGER_NAME),
            user_id=UserID(str(after.id)),
            before=NicknameChangelogBefore(before.nick or ""),
            after=NicknameChangelogAfter(after.nick or ""),
        )

        try:
            response = await self._record_nickname_change_usecase.execute(request)

            if not response.is_success:
                logfire.error(
                    "Failed to record nickname change: {message}",
                    message=response.message,
                )

        except Exception as error:
            logfire.error(
                "Exception occurred while recording nickname change: {error}",
                error=str(error),
            )

            # Send error embed to the configured channel or guild's system channel
            channel = await self._get_error_notification_channel(after.guild)
            if channel:
                await send_error_embed(
                    channel,
                    error,
                    "recording nickname change",
                )

    async def _get_error_notification_channel(
        self, guild: discord.Guild
    ) -> discord.abc.Messageable | None:
        """Get the channel for error notifications.

        Returns the configured error notification channel if set,
        otherwise falls back to the guild's system channel.
        """
        channel_id = self._config.ERROR_NOTIFICATION_CHANNEL_ID
        if channel_id is not None:
            channel = self.get_channel(channel_id)
            if channel is not None and isinstance(channel, discord.abc.Messageable):
                return channel
            # If channel not found in cache, try fetching it
            try:
                fetched_channel = await self.fetch_channel(channel_id)
                if isinstance(fetched_channel, discord.abc.Messageable):
                    return fetched_channel
            except discord.DiscordException:
                logfire.warning(
                    "Failed to fetch error notification channel: {channel_id}",
                    channel_id=channel_id,
                )
        return guild.system_channel

    def run_bot(self) -> None:
        """Run the Discord bot."""
        self.run(self._config.DISCORD_TOKEN)
