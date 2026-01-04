from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from ulid import ULID

from src.system.domain.interface.repository.common.response import (
    RepositoryResponse,
    RepositoryResultStatusEnum,
    RepositoryResponseStatusEnum,
    RepositoryFailedResponseEnum,
)
from src.system.domain.model.messenger import Messenger
from src.system.domain.model.nickname import NicknameChangelog
from src.system.domain.model.user import User
from src.system.domain.value.messenger import (
    MessengerRecordID,
    MessengerCreatedAt,
    MessengerUpdatedAt,
    MessengerName,
)
from src.system.domain.value.nickname import (
    NicknameChangelogRecordID,
    NicknameChangelogCreatedAt,
    NicknameChangelogUserRecordID,
    NicknameChangelogBefore,
    NicknameChangelogAfter,
)
from src.system.domain.value.user import (
    UserRecordID,
    UserCreatedAt,
    UserUpdatedAt,
    UserMessengerRecordID,
    UserID,
)
from src.system.usecase.nickname.dto import RecordNicknameChangeRequest
from src.system.usecase.nickname.record_nickname_change import (
    RecordNicknameChangeUsecase,
)
from src.system.util.id import generate_ulid


@pytest.fixture
def test_ulid() -> ULID:
    return generate_ulid()


@pytest.fixture
def test_datetime() -> datetime:
    return datetime(2023, 1, 1, 12, 0, 0)


@pytest.fixture
def domain_messenger(test_ulid: ULID, test_datetime: datetime) -> Messenger:
    return Messenger(
        record_id=MessengerRecordID(root=test_ulid),
        created_at=MessengerCreatedAt(root=test_datetime),
        updated_at=MessengerUpdatedAt(root=test_datetime),
        name=MessengerName(root="discord"),
    )


@pytest.fixture
def domain_user(test_ulid: ULID, test_datetime: datetime) -> User:
    return User(
        record_id=UserRecordID(root=test_ulid),
        created_at=UserCreatedAt(root=test_datetime),
        updated_at=UserUpdatedAt(root=test_datetime),
        messenger_record_id=UserMessengerRecordID(root=test_ulid),
        id=UserID(root="123456789"),
    )


@pytest.fixture
def domain_nickname_changelog(
    test_ulid: ULID, test_datetime: datetime
) -> NicknameChangelog:
    return NicknameChangelog(
        record_id=NicknameChangelogRecordID(root=test_ulid),
        created_at=NicknameChangelogCreatedAt(root=test_datetime),
        user_record_id=NicknameChangelogUserRecordID(root=test_ulid),
        before=NicknameChangelogBefore(root="old_nick"),
        after=NicknameChangelogAfter(root="new_nick"),
    )


@pytest.fixture
def request_dto() -> RecordNicknameChangeRequest:
    return RecordNicknameChangeRequest(
        messenger_name=MessengerName(root="discord"),
        user_id=UserID(root="123456789"),
        before=NicknameChangelogBefore(root="old_nick"),
        after=NicknameChangelogAfter(root="new_nick"),
    )


class TestRecordNicknameChangeUsecaseExecute:
    @pytest.mark.asyncio
    async def test_execute_success(
        self,
        request_dto: RecordNicknameChangeRequest,
        domain_messenger: Messenger,
        domain_user: User,
        domain_nickname_changelog: NicknameChangelog,
    ) -> None:
        mock_messenger_repository = MagicMock()
        mock_messenger_repository.get_by_name = AsyncMock(
            return_value=RepositoryResponse(
                response=domain_messenger,
                is_success=RepositoryResultStatusEnum.SUCCESS,
                status=RepositoryResponseStatusEnum.READ,
            )
        )

        mock_user_repository = MagicMock()
        mock_user_repository.get_or_create = AsyncMock(
            return_value=RepositoryResponse(
                response=domain_user,
                is_success=RepositoryResultStatusEnum.SUCCESS,
                status=RepositoryResponseStatusEnum.CREATED,
            )
        )

        mock_nickname_changelog_repository = MagicMock()
        mock_nickname_changelog_repository.create = AsyncMock(
            return_value=RepositoryResponse(
                response=domain_nickname_changelog,
                is_success=RepositoryResultStatusEnum.SUCCESS,
                status=RepositoryResponseStatusEnum.CREATED,
            )
        )

        usecase = RecordNicknameChangeUsecase(
            messenger_repository=mock_messenger_repository,
            user_repository=mock_user_repository,
            nickname_changelog_repository=mock_nickname_changelog_repository,
        )

        with (
            patch(
                "src.system.usecase.nickname.record_nickname_change.utcnow"
            ) as mock_utcnow,
            patch(
                "src.system.usecase.nickname.record_nickname_change.generate_ulid"
            ) as mock_generate_ulid,
        ):
            mock_utcnow.return_value = datetime(2023, 1, 1, 12, 0, 0)
            mock_generate_ulid.return_value = generate_ulid()

            result = await usecase.execute(request_dto)

        assert result.is_success is True
        assert result.message is None
        mock_messenger_repository.get_by_name.assert_awaited_once()
        mock_user_repository.get_or_create.assert_awaited_once()
        mock_nickname_changelog_repository.create.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_execute_messenger_not_found(
        self,
        request_dto: RecordNicknameChangeRequest,
    ) -> None:
        mock_messenger_repository = MagicMock()
        mock_messenger_repository.get_by_name = AsyncMock(
            return_value=RepositoryResponse(
                response=None,
                is_success=RepositoryResultStatusEnum.SUCCESS,
                status=RepositoryResponseStatusEnum.READ,
            )
        )

        mock_user_repository = MagicMock()
        mock_nickname_changelog_repository = MagicMock()

        usecase = RecordNicknameChangeUsecase(
            messenger_repository=mock_messenger_repository,
            user_repository=mock_user_repository,
            nickname_changelog_repository=mock_nickname_changelog_repository,
        )

        result = await usecase.execute(request_dto)

        assert result.is_success is False
        assert result.message is not None
        assert "discord" in result.message
        mock_messenger_repository.get_by_name.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_execute_messenger_repository_error(
        self,
        request_dto: RecordNicknameChangeRequest,
    ) -> None:
        mock_messenger_repository = MagicMock()
        mock_messenger_repository.get_by_name = AsyncMock(
            return_value=RepositoryResponse(
                response=None,
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
                reason=RepositoryFailedResponseEnum.UNKNOWN,
                message="Database error",
            )
        )

        mock_user_repository = MagicMock()
        mock_nickname_changelog_repository = MagicMock()

        usecase = RecordNicknameChangeUsecase(
            messenger_repository=mock_messenger_repository,
            user_repository=mock_user_repository,
            nickname_changelog_repository=mock_nickname_changelog_repository,
        )

        result = await usecase.execute(request_dto)

        assert result.is_success is False
        assert result.message == "Database error"

    @pytest.mark.asyncio
    async def test_execute_user_repository_error(
        self,
        request_dto: RecordNicknameChangeRequest,
        domain_messenger: Messenger,
    ) -> None:
        mock_messenger_repository = MagicMock()
        mock_messenger_repository.get_by_name = AsyncMock(
            return_value=RepositoryResponse(
                response=domain_messenger,
                is_success=RepositoryResultStatusEnum.SUCCESS,
                status=RepositoryResponseStatusEnum.READ,
            )
        )

        mock_user_repository = MagicMock()
        mock_user_repository.get_or_create = AsyncMock(
            return_value=RepositoryResponse(
                response=None,
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
                reason=RepositoryFailedResponseEnum.UNKNOWN,
                message="User creation failed",
            )
        )

        mock_nickname_changelog_repository = MagicMock()

        usecase = RecordNicknameChangeUsecase(
            messenger_repository=mock_messenger_repository,
            user_repository=mock_user_repository,
            nickname_changelog_repository=mock_nickname_changelog_repository,
        )

        with (
            patch(
                "src.system.usecase.nickname.record_nickname_change.utcnow"
            ) as mock_utcnow,
            patch(
                "src.system.usecase.nickname.record_nickname_change.generate_ulid"
            ) as mock_generate_ulid,
        ):
            mock_utcnow.return_value = datetime(2023, 1, 1, 12, 0, 0)
            mock_generate_ulid.return_value = generate_ulid()

            result = await usecase.execute(request_dto)

        assert result.is_success is False
        assert result.message == "User creation failed"

    @pytest.mark.asyncio
    async def test_execute_user_response_none(
        self,
        request_dto: RecordNicknameChangeRequest,
        domain_messenger: Messenger,
    ) -> None:
        mock_messenger_repository = MagicMock()
        mock_messenger_repository.get_by_name = AsyncMock(
            return_value=RepositoryResponse(
                response=domain_messenger,
                is_success=RepositoryResultStatusEnum.SUCCESS,
                status=RepositoryResponseStatusEnum.READ,
            )
        )

        mock_user_repository = MagicMock()
        mock_user_repository.get_or_create = AsyncMock(
            return_value=RepositoryResponse(
                response=None,
                is_success=RepositoryResultStatusEnum.SUCCESS,
                status=RepositoryResponseStatusEnum.READ,
            )
        )

        mock_nickname_changelog_repository = MagicMock()

        usecase = RecordNicknameChangeUsecase(
            messenger_repository=mock_messenger_repository,
            user_repository=mock_user_repository,
            nickname_changelog_repository=mock_nickname_changelog_repository,
        )

        with (
            patch(
                "src.system.usecase.nickname.record_nickname_change.utcnow"
            ) as mock_utcnow,
            patch(
                "src.system.usecase.nickname.record_nickname_change.generate_ulid"
            ) as mock_generate_ulid,
        ):
            mock_utcnow.return_value = datetime(2023, 1, 1, 12, 0, 0)
            mock_generate_ulid.return_value = generate_ulid()

            result = await usecase.execute(request_dto)

        assert result.is_success is False
        assert result.message == "Failed to get or create user"

    @pytest.mark.asyncio
    async def test_execute_nickname_changelog_repository_error(
        self,
        request_dto: RecordNicknameChangeRequest,
        domain_messenger: Messenger,
        domain_user: User,
    ) -> None:
        mock_messenger_repository = MagicMock()
        mock_messenger_repository.get_by_name = AsyncMock(
            return_value=RepositoryResponse(
                response=domain_messenger,
                is_success=RepositoryResultStatusEnum.SUCCESS,
                status=RepositoryResponseStatusEnum.READ,
            )
        )

        mock_user_repository = MagicMock()
        mock_user_repository.get_or_create = AsyncMock(
            return_value=RepositoryResponse(
                response=domain_user,
                is_success=RepositoryResultStatusEnum.SUCCESS,
                status=RepositoryResponseStatusEnum.CREATED,
            )
        )

        mock_nickname_changelog_repository = MagicMock()
        mock_nickname_changelog_repository.create = AsyncMock(
            return_value=RepositoryResponse(
                response=None,
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
                reason=RepositoryFailedResponseEnum.UNKNOWN,
                message="Changelog creation failed",
            )
        )

        usecase = RecordNicknameChangeUsecase(
            messenger_repository=mock_messenger_repository,
            user_repository=mock_user_repository,
            nickname_changelog_repository=mock_nickname_changelog_repository,
        )

        with (
            patch(
                "src.system.usecase.nickname.record_nickname_change.utcnow"
            ) as mock_utcnow,
            patch(
                "src.system.usecase.nickname.record_nickname_change.generate_ulid"
            ) as mock_generate_ulid,
        ):
            mock_utcnow.return_value = datetime(2023, 1, 1, 12, 0, 0)
            mock_generate_ulid.return_value = generate_ulid()

            result = await usecase.execute(request_dto)

        assert result.is_success is False
        assert result.message == "Changelog creation failed"
