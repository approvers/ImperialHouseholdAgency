from pydantic import Field
from pydantic_settings import BaseSettings

from src.domain.config import DomainConfigIF
from src.ui.discord.config import DiscordConfigIF


class ImperialHouseholdAgencyConfig(DomainConfigIF, DiscordConfigIF, BaseSettings):
    DISCORD_TOKEN: str = Field(
        description="Discord bot token",
    )
