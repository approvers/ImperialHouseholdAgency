from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.system.usecase.nickname.dto import RecordNicknameChangeResponse
from src.system.ui.discord.bot import DiscordBot


@pytest.fixture
def mock_config() -> MagicMock:
    config = MagicMock()
    config.DISCORD_TOKEN = "test_token"
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
        mock_system_channel.send = AsyncMock()
        mock_after_member.guild.system_channel = mock_system_channel

        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch("src.system.ui.discord.bot.logfire") as mock_logfire,
            patch("src.system.ui.discord.bot.sentry_sdk") as mock_sentry,
            patch("src.system.ui.discord.bot.trace") as mock_trace,
        ):
            mock_sentry.capture_exception.return_value = "test-event-id"
            mock_span_context = MagicMock()
            mock_span_context.is_valid = True
            mock_span_context.trace_id = 0x1234567890ABCDEF1234567890ABCDEF
            mock_span = MagicMock()
            mock_span.get_span_context.return_value = mock_span_context
            mock_trace.get_current_span.return_value = mock_span

            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            await bot.on_member_update(mock_before_member, mock_after_member)

        mock_logfire.error.assert_called()
        mock_sentry.capture_exception.assert_called_once_with(test_error)
        mock_system_channel.send.assert_awaited_once()

        # Verify the embed was sent with correct content
        embed = mock_system_channel.send.call_args.kwargs["embed"]
        assert embed.title == "Error Occurred"
        assert "RuntimeError" in str(embed.fields[0].value)

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

            await bot.on_member_update(mock_before_member, mock_after_member)

        mock_logfire.error.assert_called()


class TestDiscordBotSendErrorEmbed:
    @pytest.mark.asyncio
    async def test_send_error_embed_discord_exception_logs_error(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        import discord

        mock_channel = MagicMock()
        mock_channel.send = AsyncMock(
            side_effect=discord.DiscordException("Send failed")
        )

        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch("src.system.ui.discord.bot.logfire") as mock_logfire,
            patch("src.system.ui.discord.bot.sentry_sdk") as mock_sentry,
            patch("src.system.ui.discord.bot.trace") as mock_trace,
        ):
            mock_sentry.capture_exception.return_value = None
            mock_span_context = MagicMock()
            mock_span_context.is_valid = False
            mock_span = MagicMock()
            mock_span.get_span_context.return_value = mock_span_context
            mock_trace.get_current_span.return_value = mock_span

            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            await bot._send_error_embed(
                mock_channel,
                RuntimeError("Test error"),
                "testing",
            )

        mock_logfire.error.assert_called_once()
        assert "Failed to send error embed" in str(mock_logfire.error.call_args)


class TestDiscordBotGetTraceId:
    def test_get_trace_id_valid_span(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch("src.system.ui.discord.bot.trace") as mock_trace,
        ):
            mock_span_context = MagicMock()
            mock_span_context.is_valid = True
            mock_span_context.trace_id = 0x1234567890ABCDEF1234567890ABCDEF
            mock_span = MagicMock()
            mock_span.get_span_context.return_value = mock_span_context
            mock_trace.get_current_span.return_value = mock_span

            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            trace_id = bot._get_trace_id()

        assert trace_id == "1234567890abcdef1234567890abcdef"

    def test_get_trace_id_invalid_span(
        self,
        mock_config: MagicMock,
        mock_usecase: MagicMock,
    ) -> None:
        with (
            patch.object(DiscordBot, "__init__", lambda self, *args, **kwargs: None),
            patch("src.system.ui.discord.bot.trace") as mock_trace,
        ):
            mock_span_context = MagicMock()
            mock_span_context.is_valid = False
            mock_span = MagicMock()
            mock_span.get_span_context.return_value = mock_span_context
            mock_trace.get_current_span.return_value = mock_span

            bot = DiscordBot.__new__(DiscordBot)
            bot._config = mock_config
            bot._record_nickname_change_usecase = mock_usecase

            trace_id = bot._get_trace_id()

        assert trace_id is None


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
