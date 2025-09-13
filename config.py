from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.domain.config import DomainConfigIF, EnvironmentEnum
from src.infrastructure.repository.sqlalchemy.config import SQLAlchemyConfigIF
from src.ui.discord.config import DiscordConfigIF


class BaseConfig(DomainConfigIF, SQLAlchemyConfigIF, DiscordConfigIF, BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./env/test.env", env_file_encoding="utf-8", extra="allow"
    )

    # domain
    environment: EnvironmentEnum = EnvironmentEnum.TEST

    @property
    def ENVIRONMENT(self) -> EnvironmentEnum:
        return self.environment

    # SQLAlchemy
    database_url: str = Field(alias="DATABASE_URL")

    @property
    def DATABASE_URL(self) -> str:
        return self.environment.name

    # Discord
    discord_token: str = Field(alias="DISCORD_TOKEN")

    @property
    def DISCORD_TOKEN(self) -> str:
        return self.discord_token


class TestConfig(BaseConfig):
    model_config = SettingsConfigDict(
        env_file="./env/test.env", env_file_encoding="utf-8"
    )

    environment: EnvironmentEnum = EnvironmentEnum.TEST


class DevelopConfig(BaseConfig):
    model_config = SettingsConfigDict(
        env_file="./env/local.env", env_file_encoding="utf-8"
    )

    environment: EnvironmentEnum = EnvironmentEnum.DEVELOPMENT


class ProductionConfig(BaseConfig):
    model_config = SettingsConfigDict(
        env_file="./env/local.env", env_file_encoding="utf-8"
    )

    environment: EnvironmentEnum = EnvironmentEnum.PRODUCTION
