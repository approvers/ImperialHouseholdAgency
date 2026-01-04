from unittest.mock import MagicMock

from injector import Injector, Module, provider, singleton

from src.system.di.module.ui.discord.bot.module import DiscordBotModule
from src.system.ui.discord.bot import DiscordBot
from src.system.ui.discord.config import DiscordConfigIf
from src.system.usecase.nickname.interface import RecordNicknameChangeUsecaseIf


class MockConfigModule(Module):
    @provider
    @singleton
    def provide_discord_config(self) -> DiscordConfigIf:
        config = MagicMock(spec=DiscordConfigIf)
        config.DISCORD_TOKEN = "test_token"
        return config


class MockUsecaseModule(Module):
    @provider
    @singleton
    def provide_record_nickname_change_usecase(
        self,
    ) -> RecordNicknameChangeUsecaseIf:
        return MagicMock(spec=RecordNicknameChangeUsecaseIf)


class TestDiscordBotModule:
    def test_binds_discord_bot(self) -> None:
        injector = Injector(
            [MockConfigModule(), MockUsecaseModule(), DiscordBotModule()],
            auto_bind=False,
        )

        instance = injector.get(DiscordBot)

        assert isinstance(instance, DiscordBot)
