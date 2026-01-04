from injector import Binder, Module, singleton

from src.system.usecase.nickname.interface import RecordNicknameChangeUsecaseIf
from src.system.usecase.nickname.record_nickname_change import (
    RecordNicknameChangeUsecase,
)


class NicknameUsecaseModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            interface=RecordNicknameChangeUsecaseIf,  # type: ignore[type-abstract]
            to=RecordNicknameChangeUsecase,
            scope=singleton,
        )
