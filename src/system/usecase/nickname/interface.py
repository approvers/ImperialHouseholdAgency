from src.system.usecase.base.interface import UsecaseIf
from src.system.usecase.nickname.dto import (
    RecordNicknameChangeRequest,
    RecordNicknameChangeResponse,
)


class RecordNicknameChangeUsecaseIf(
    UsecaseIf[RecordNicknameChangeRequest, RecordNicknameChangeResponse]
):
    """Interface for the use case that records nickname changes."""

    pass
