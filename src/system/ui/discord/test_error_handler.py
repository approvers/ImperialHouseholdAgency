from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest

from src.system.ui.discord.error_handler import (
    _ERROR_THUMBNAIL_URL,
    send_error_embed,
)


class TestSendErrorEmbed:
    @pytest.mark.asyncio
    async def test_sends_embed_with_error_details(self) -> None:
        mock_channel = MagicMock()
        mock_channel.send = AsyncMock()
        test_error = RuntimeError("Test exception message")

        with (
            patch("src.system.ui.discord.error_handler.sentry_sdk") as mock_sentry,
            patch(
                "src.system.ui.discord.error_handler.get_current_trace_id"
            ) as mock_get_trace_id,
        ):
            mock_sentry.capture_exception.return_value = "test-event-id"
            mock_get_trace_id.return_value = "1234567890abcdef1234567890abcdef"

            await send_error_embed(mock_channel, test_error, "testing")

        mock_sentry.capture_exception.assert_called_once_with(test_error)
        mock_channel.send.assert_awaited_once()

        embed = mock_channel.send.call_args.kwargs["embed"]
        assert embed.title == "Error Occurred"
        assert "testing" in embed.description
        assert embed.thumbnail.url == _ERROR_THUMBNAIL_URL
        assert embed.fields[0].value == "RuntimeError"
        assert embed.fields[1].value == "Test exception message"
        assert embed.fields[2].value == "test-event-id"
        assert embed.fields[3].value == "1234567890abcdef1234567890abcdef"

    @pytest.mark.asyncio
    async def test_sends_embed_without_sentry_event_id(self) -> None:
        mock_channel = MagicMock()
        mock_channel.send = AsyncMock()
        test_error = RuntimeError("Test exception")

        with (
            patch("src.system.ui.discord.error_handler.sentry_sdk") as mock_sentry,
            patch(
                "src.system.ui.discord.error_handler.get_current_trace_id"
            ) as mock_get_trace_id,
        ):
            mock_sentry.capture_exception.return_value = None
            mock_get_trace_id.return_value = "trace-id-123"

            await send_error_embed(mock_channel, test_error, "testing")

        embed = mock_channel.send.call_args.kwargs["embed"]
        field_names = [f.name for f in embed.fields]
        assert "Sentry Event ID" not in field_names
        assert "Trace ID" in field_names

    @pytest.mark.asyncio
    async def test_sends_embed_without_trace_id(self) -> None:
        mock_channel = MagicMock()
        mock_channel.send = AsyncMock()
        test_error = RuntimeError("Test exception")

        with (
            patch("src.system.ui.discord.error_handler.sentry_sdk") as mock_sentry,
            patch(
                "src.system.ui.discord.error_handler.get_current_trace_id"
            ) as mock_get_trace_id,
        ):
            mock_sentry.capture_exception.return_value = "event-123"
            mock_get_trace_id.return_value = None

            await send_error_embed(mock_channel, test_error, "testing")

        embed = mock_channel.send.call_args.kwargs["embed"]
        field_names = [f.name for f in embed.fields]
        assert "Sentry Event ID" in field_names
        assert "Trace ID" not in field_names

    @pytest.mark.asyncio
    async def test_truncates_long_error_message(self) -> None:
        mock_channel = MagicMock()
        mock_channel.send = AsyncMock()
        long_message = "x" * 2000
        test_error = RuntimeError(long_message)

        with (
            patch("src.system.ui.discord.error_handler.sentry_sdk") as mock_sentry,
            patch(
                "src.system.ui.discord.error_handler.get_current_trace_id"
            ) as mock_get_trace_id,
        ):
            mock_sentry.capture_exception.return_value = None
            mock_get_trace_id.return_value = None

            await send_error_embed(mock_channel, test_error, "testing")

        embed = mock_channel.send.call_args.kwargs["embed"]
        assert len(embed.fields[1].value) == 1024

    @pytest.mark.asyncio
    async def test_logs_error_when_send_fails(self) -> None:
        mock_channel = MagicMock()
        mock_channel.send = AsyncMock(
            side_effect=discord.DiscordException("Send failed")
        )
        test_error = RuntimeError("Test exception")

        with (
            patch("src.system.ui.discord.error_handler.sentry_sdk") as mock_sentry,
            patch(
                "src.system.ui.discord.error_handler.get_current_trace_id"
            ) as mock_get_trace_id,
            patch("src.system.ui.discord.error_handler.logfire") as mock_logfire,
        ):
            mock_sentry.capture_exception.return_value = None
            mock_get_trace_id.return_value = None

            await send_error_embed(mock_channel, test_error, "testing")

        mock_logfire.error.assert_called_once()
        assert "Failed to send error embed" in str(mock_logfire.error.call_args)
