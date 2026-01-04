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

        response = await self._record_nickname_change_usecase.execute(request)

        if not response.is_success:
            logfire.error(
                "Failed to record nickname change: {message}",
                message=response.message,
            )

    def run_bot(self) -> None:
        """Run the Discord bot."""
        self.run(self._config.DISCORD_TOKEN)
