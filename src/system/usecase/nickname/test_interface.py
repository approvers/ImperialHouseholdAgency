from abc import ABC

from src.system.usecase.nickname.interface import RecordNicknameChangeUsecaseIf


class TestRecordNicknameChangeUsecaseIf:
    def test_is_abstract(self) -> None:
        assert issubclass(RecordNicknameChangeUsecaseIf, ABC)
