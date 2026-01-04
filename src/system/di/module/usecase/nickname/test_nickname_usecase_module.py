from unittest.mock import MagicMock

from injector import Injector, Module, provider, singleton

from src.system.di.module.usecase.nickname.module import NicknameUsecaseModule
from src.system.domain.interface.repository.messenger import MessengerRepository
from src.system.domain.interface.repository.nickname import NicknameChangelogRepository
from src.system.domain.interface.repository.user import UserRepository
from src.system.usecase.nickname.interface import RecordNicknameChangeUsecaseIf
from src.system.usecase.nickname.record_nickname_change import (
    RecordNicknameChangeUsecase,
)


class MockRepositoryModule(Module):
    @provider
    @singleton
    def provide_messenger_repository(self) -> MessengerRepository:
        return MagicMock(spec=MessengerRepository)

    @provider
    @singleton
    def provide_user_repository(self) -> UserRepository:
        return MagicMock(spec=UserRepository)

    @provider
    @singleton
    def provide_nickname_changelog_repository(self) -> NicknameChangelogRepository:
        return MagicMock(spec=NicknameChangelogRepository)


class TestNicknameUsecaseModule:
    def test_binds_record_nickname_change_usecase(self) -> None:
        injector = Injector(
            [MockRepositoryModule(), NicknameUsecaseModule()], auto_bind=False
        )

        instance = injector.get(RecordNicknameChangeUsecaseIf)

        assert isinstance(instance, RecordNicknameChangeUsecase)
