import os

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.system.domain.config import DomainConfigIf, EnvironmentEnum
from src.system.infrastructure.repository.sqlalchemy.config import SQLAlchemyConfigIf
from src.system.infrastructure.sentry.config import SentryConfigIf
from src.system.ui.discord.config import DiscordConfigIf


class BaseConfig(
    DomainConfigIf, SQLAlchemyConfigIf, DiscordConfigIf, SentryConfigIf, BaseSettings
):
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
        return self.database_url

    # Discord
    discord_token: str = Field(alias="DISCORD_TOKEN")

    @property
    def DISCORD_TOKEN(self) -> str:
        return self.discord_token

    # Sentry
    sentry_dsn: HttpUrl = Field(
        default=HttpUrl(
            "https://18f318e974680126187592b8001394df@o4509562192330752.ingest.de.sentry.io/4510019968499792"
        ),
        alias="SENTRY_DSN",
    )
    sentry_env: str | None = Field(default=None, alias="SENTRY_ENV")

    @property
    def SENTRY_DSN(self) -> str:
        return str(self.sentry_dsn)

    @property
    def SENTRY_ENV(self) -> str:
        if self.sentry_env:
            return self.sentry_env

        return self.ENVIRONMENT.name


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


# noinspection PyArgumentList
def get_config(environment: EnvironmentEnum) -> BaseConfig:
    match environment:
        case EnvironmentEnum.TEST:
            return TestConfig()

        case EnvironmentEnum.DEVELOPMENT:
            return DevelopConfig()

        case EnvironmentEnum.PRODUCTION:
            return ProductionConfig()


def get_config_for_current_env() -> BaseConfig:
    # noinspection SpellCheckingInspection
    envvar = os.getenv("ENVIRONMENT")
    env: EnvironmentEnum = EnvironmentEnum.TEST

    if envvar is not None:
        env = EnvironmentEnum(envvar)

    return get_config(env)
