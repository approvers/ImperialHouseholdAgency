from pydantic import Field

from src.system.domain.value.messenger import MessengerName
from src.system.domain.value.nickname import (
    NicknameChangelogBefore,
    NicknameChangelogAfter,
)
from src.system.domain.value.user import UserID
from src.system.usecase.base.dto import UsecaseRequest, UsecaseResponse


class RecordNicknameChangeRequest(UsecaseRequest):
    """Request DTO for recording a nickname change.

    Attributes:
        messenger_name: The name of the messenger platform.
        user_id: The user's ID on the messenger platform.
        before: The previous nickname.
        after: The new nickname.
    """

    messenger_name: MessengerName
    user_id: UserID
    before: NicknameChangelogBefore
    after: NicknameChangelogAfter


class RecordNicknameChangeResponse(UsecaseResponse):
    """Response DTO for recording a nickname change.

    Attributes:
        is_success: Whether the operation was successful.
        message: A message describing the result.
    """

    is_success: bool
    message: str | None = Field(default=None)
