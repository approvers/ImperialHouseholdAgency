from src.system.domain.value.messenger import MessengerName
from src.system.domain.value.nickname import (
    NicknameChangelogBefore,
    NicknameChangelogAfter,
)
from src.system.domain.value.user import UserID
from src.system.usecase.nickname.dto import (
    RecordNicknameChangeRequest,
    RecordNicknameChangeResponse,
)


class TestRecordNicknameChangeRequest:
    def test_create_request(self) -> None:
        request = RecordNicknameChangeRequest(
            messenger_name=MessengerName(root="discord"),
            user_id=UserID(root="123456789"),
            before=NicknameChangelogBefore(root="old_nick"),
            after=NicknameChangelogAfter(root="new_nick"),
        )

        assert request.messenger_name.root == "discord"
        assert request.user_id.root == "123456789"
        assert request.before.root == "old_nick"
        assert request.after.root == "new_nick"


class TestRecordNicknameChangeResponse:
    def test_create_response_success(self) -> None:
        response = RecordNicknameChangeResponse(is_success=True)

        assert response.is_success is True
        assert response.message is None

    def test_create_response_failure(self) -> None:
        response = RecordNicknameChangeResponse(
            is_success=False, message="Error message"
        )

        assert response.is_success is False
        assert response.message == "Error message"
