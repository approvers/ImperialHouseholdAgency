from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.system.usecase.nickname.dto import RecordNicknameChangeResponse
from src.system.ui.discord.bot import DiscordBot


@pytest.fixture
def mock_config() -> MagicMock:
    config = MagicMock()
    config.DISCORD_TOKEN = "test_token"
    config.ERROR_NOTIFICATION_CHANNEL_ID = None
    return config


@pytest.fixture
def mock_usecase() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_before_member() -> MagicMock:
    member = MagicMock()
    member.nick = "old_nickname"
    member.id = 123456789
    return member


@pytest.fixture
def mock_after_member() -> MagicMock:
    member = MagicMock()
    member.nick = "new_nickname"
    member.id = 123456789
    return member


class TestDiscordBotOnMemberUpdate:
    @pytest.mark.asyncio
    async def test_on_member_update_nickname_changed(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
        mock_before_member: MagicMock,
        mock_after_member: MagicMock,
    ) -> None:
        mock_usecase.execute = AsyncMock(
            return_value=RecordNicknameChangeResponse(is_success=True)
        )

        with patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            await bot.on_member_update(mock_before_member, mock_after_member)

        mock_usecase.execute.assert_awaited_once()
        call_args = mock_usecase.execute.call_args[0][0]
        assert call_args.messenger_name.root == "discord"
        assert call_args.user_id.root == "123456789"
        assert call_args.before.root == "old_nickname"
        assert call_args.after.root == "new_nickname"

    @pytest.mark.asyncio
    async def test_on_member_update_nickname_unchanged(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        before_member = MagicMock()
        before_member.nick = "same_nickname"
        before_member.id = 123456789

        after_member = MagicMock()
        after_member.nick = "same_nickname"
        after_member.id = 123456789

        with patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            await bot.on_member_update(before_member, after_member)

        mock_usecase.execute.assert_not_called()

    @pytest.mark.asyncio
    async def test_on_member_update_nickname_none_to_value(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        before_member = MagicMock()
        before_member.nick = None
        before_member.id = 123456789

        after_member = MagicMock()
        after_member.nick = "new_nickname"
        after_member.id = 123456789

        mock_usecase.execute = AsyncMock(
            return_value=RecordNicknameChangeResponse(is_success=True)
        )

        with patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            await bot.on_member_update(before_member, after_member)

        mock_usecase.execute.assert_awaited_once()
        call_args = mock_usecase.execute.call_args[0][0]
        assert call_args.before.root == ""
        assert call_args.after.root == "new_nickname"

    @pytest.mark.asyncio
    async def test_on_member_update_nickname_value_to_none(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        before_member = MagicMock()
        before_member.nick = "old_nickname"
        before_member.id = 123456789

        after_member = MagicMock()
        after_member.nick = None
        after_member.id = 123456789

        mock_usecase.execute = AsyncMock(
            return_value=RecordNicknameChangeResponse(is_success=True)
        )

        with patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            await bot.on_member_update(before_member, after_member)

        mock_usecase.execute.assert_awaited_once()
        call_args = mock_usecase.execute.call_args[0][0]
        assert call_args.before.root == "old_nickname"
        assert call_args.after.root == ""

    @pytest.mark.asyncio
    async def test_on_member_update_usecase_failure_logs_error(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
        mock_before_member: MagicMock,
        mock_after_member: MagicMock,
    ) -> None:
        mock_usecase.execute = AsyncMock(
            return_value=RecordNicknameChangeResponse(
                is_success=False, message="Test error"
            )
        )

        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch("src.system.ui.discord.bot.logfire") as mock_logfire,
        ):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            await bot.on_member_update(mock_before_member, mock_after_member)

        mock_usecase.execute.assert_awaited_once()
        mock_logfire.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_on_member_update_exception_sends_error_embed(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
        mock_before_member: MagicMock,
        mock_after_member: MagicMock,
    ) -> None:
        test_error = RuntimeError("Test exception")
        mock_usecase.execute = AsyncMock(side_effect=test_error)

        mock_system_channel = MagicMock()
        mock_after_member.guild.system_channel = mock_system_channel

        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch("src.system.ui.discord.bot.logfire") as mock_logfire,
            patch(
                "src.system.ui.discord.bot.send_error_embed"
            ) as mock_send_error_embed,
        ):
            mock_send_error_embed.return_value = None

            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase
            bot.get_channel = MagicMock(return_value=None)

            await bot.on_member_update(mock_before_member, mock_after_member)

        mock_logfire.error.assert_called()
        mock_send_error_embed.assert_awaited_once_with(
            mock_system_channel,
            test_error,
            "recording nickname change",
        )

    @pytest.mark.asyncio
    async def test_on_member_update_exception_no_system_channel(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
        mock_before_member: MagicMock,
        mock_after_member: MagicMock,
    ) -> None:
        test_error = RuntimeError("Test exception")
        mock_usecase.execute = AsyncMock(side_effect=test_error)
        mock_after_member.guild.system_channel = None

        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch("src.system.ui.discord.bot.logfire") as mock_logfire,
        ):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase
            bot.get_channel = MagicMock(return_value=None)

            await bot.on_member_update(mock_before_member, mock_after_member)

        mock_logfire.error.assert_called()


class TestDiscordBotGetErrorNotificationChannel:
    @pytest.mark.asyncio
    async def test_returns_configured_channel_from_cache(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        import discord

        mock_config.ERROR_NOTIFICATION_CHANNEL_ID = 123456789
        mock_channel = MagicMock(spec=discord.abc.Messageable)
        mock_guild = MagicMock()

        with patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase
            bot.get_channel = MagicMock(return_value=mock_channel)

            result = await bot._get_error_notification_channel(mock_guild)

        assert result == mock_channel
        bot.get_channel.assert_called_once_with(123456789)

    @pytest.mark.asyncio
    async def test_fetches_channel_when_not_in_cache(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        import discord

        mock_config.ERROR_NOTIFICATION_CHANNEL_ID = 123456789
        mock_channel = MagicMock(spec=discord.abc.Messageable)
        mock_guild = MagicMock()

        with patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase
            bot.get_channel = MagicMock(return_value=None)
            bot.fetch_channel = AsyncMock(return_value=mock_channel)

            result = await bot._get_error_notification_channel(mock_guild)

        assert result == mock_channel
        bot.fetch_channel.assert_awaited_once_with(123456789)

    @pytest.mark.asyncio
    async def test_falls_back_to_system_channel_on_fetch_error(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        import discord

        mock_config.ERROR_NOTIFICATION_CHANNEL_ID = 123456789
        mock_system_channel = MagicMock()
        mock_guild = MagicMock()
        mock_guild.system_channel = mock_system_channel

        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch("src.system.ui.discord.bot.logfire") as mock_logfire,
        ):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase
            bot.get_channel = MagicMock(return_value=None)
            bot.fetch_channel = AsyncMock(
                side_effect=discord.DiscordException("Channel not found")
            )

            result = await bot._get_error_notification_channel(mock_guild)

        assert result == mock_system_channel
        mock_logfire.warning.assert_called_once()

    @pytest.mark.asyncio
    async def test_returns_system_channel_when_no_config(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        mock_config.ERROR_NOTIFICATION_CHANNEL_ID = None
        mock_system_channel = MagicMock()
        mock_guild = MagicMock()
        mock_guild.system_channel = mock_system_channel

        with patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            result = await bot._get_error_notification_channel(mock_guild)

        assert result == mock_system_channel


class TestDiscordBotOnMessage:
    @pytest.mark.asyncio
    async def test_ignores_bot_messages(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        mock_message = MagicMock()
        mock_message.author.bot = True
        mock_message.content = "!exception-test"

        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch(
                "src.system.ui.discord.bot.send_error_embed"
            ) as mock_send_error_embed,
        ):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            await bot.on_message(mock_message)

        mock_send_error_embed.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_exception_test_command_sends_error_embed(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        mock_message = MagicMock()
        mock_message.author.bot = False
        mock_message.content = "!exception-test"
        mock_channel = MagicMock()
        mock_message.channel = mock_channel

        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch("src.system.ui.discord.bot.logfire") as mock_logfire,
            patch(
                "src.system.ui.discord.bot.send_error_embed"
            ) as mock_send_error_embed,
        ):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            await bot.on_message(mock_message)

        mock_logfire.error.assert_called_once()
        mock_send_error_embed.assert_awaited_once()
        call_args = mock_send_error_embed.call_args
        assert call_args[0][0] == mock_channel
        assert isinstance(call_args[0][1], RuntimeError)
        assert call_args[0][2] == "processing test command"

    @pytest.mark.asyncio
    async def test_ignores_non_command_messages(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        mock_message = MagicMock()
        mock_message.author.bot = False
        mock_message.content = "hello world"

        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch(
                "src.system.ui.discord.bot.send_error_embed"
            ) as mock_send_error_embed,
        ):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            await bot.on_message(mock_message)

        mock_send_error_embed.assert_not_awaited()


class TestDiscordBotRunBot:
    def test_run_bot_calls_run_with_token(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch.object(DiscordBot, "run") as mock_run,
        ):
            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            bot.run_bot()

        mock_run.assert_called_once_with("test_token")
