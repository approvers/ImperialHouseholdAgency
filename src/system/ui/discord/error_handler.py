import discord
import logfire
import sentry_sdk

from src.system.infrastructure.ext.logfire.trace import get_current_trace_id

_ERROR_THUMBNAIL_URL = "https://upload.wikimedia.org/wikipedia/commons/5/5f/Red_X.svg"


async def send_error_embed(
    channel: discord.abc.Messageable,
    error: Exception,
    context: str,
) -> None:
    """Send an error embed to the specified channel.

    This function is intentionally not instrumented to avoid infinite loops
    when sending error messages fails.

    Args:
        channel: The Discord channel to send the error embed to.
        error: The exception that occurred.
        context: A description of what was happening when the error occurred.
    """
    # Capture exception to Sentry and get event ID
    event_id = sentry_sdk.capture_exception(error)

    # Get trace ID from OpenTelemetry (used by Logfire)
    trace_id = get_current_trace_id()

    embed = discord.Embed(
        title="Error Occurred",
        description=f"An error occurred while {context}.",
        color=discord.Color.red(),
    )
    embed.set_thumbnail(url=_ERROR_THUMBNAIL_URL)
    embed.add_field(name="Error Type", value=type(error).__name__, inline=True)
    embed.add_field(name="Error Message", value=str(error)[:1024], inline=False)

    if event_id:
        embed.add_field(name="Sentry Event ID", value=str(event_id), inline=True)
    if trace_id:
        embed.add_field(name="Trace ID", value=trace_id, inline=True)

    try:
        await channel.send(embed=embed)
    except discord.DiscordException as send_error:
        # Log the failure but do not attempt to send another error message
        # to avoid infinite loops
        logfire.error(
            "Failed to send error embed: {error}",
            error=str(send_error),
        )
