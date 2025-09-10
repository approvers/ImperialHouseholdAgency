from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.domain.config import DomainConfigIF
from src.ui.discord.config import DiscordConfigIF


class ImperialHouseholdAgencyConfig(DomainConfigIF, DiscordConfigIF, BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    discord_token: str = Field(alias="DISCORD_TOKEN")

    @property
    def DISCORD_TOKEN(self) -> str:
        return self.discord_token
