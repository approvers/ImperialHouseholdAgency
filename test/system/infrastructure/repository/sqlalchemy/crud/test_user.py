from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from ulid import ULID

from src.system.domain.interface.repository.common.response import (
    RepositoryResultStatusEnum,
    RepositoryResponseStatusEnum,
    RepositoryFailedResponseEnum,
)
from src.system.domain.model.user import User
from src.system.domain.value.user import (
    UserRecordID,
    UserCreatedAt,
    UserUpdatedAt,
    UserMessengerRecordID,
    UserID,
)
from src.system.infrastructure.repository.sqlalchemy.crud.user import SAUserRepository
from src.system.util.id import generate_ulid


@pytest.fixture
def test_ulid() -> ULID:
    return generate_ulid()


@pytest.fixture
def test_messenger_record_id() -> ULID:
    return generate_ulid()


@pytest.fixture
def test_datetime() -> datetime:
    return datetime(2023, 1, 1, 12, 0, 0)


@pytest.fixture
def domain_user(
    test_ulid: ULID, test_messenger_record_id: ULID, test_datetime: datetime
) -> User:
    return User(
        record_id=UserRecordID(root=test_ulid),
        created_at=UserCreatedAt(root=test_datetime),
        updated_at=UserUpdatedAt(root=test_datetime),
        messenger_record_id=UserMessengerRecordID(root=test_messenger_record_id),
        id=UserID(root="user123"),
    )


@pytest.fixture
def mock_sa_user(
    test_ulid: ULID, test_messenger_record_id: ULID, test_datetime: datetime
) -> Any:
    mock = MagicMock()
    mock.record_id = test_ulid
    mock.created_at = test_datetime
    mock.updated_at = test_datetime
    mock.messenger_record_id = test_messenger_record_id
    mock.user_id = "user123"
    return mock


class TestSAUserRepositoryCreate:
    @pytest.mark.asyncio
    async def test_create_success(
        self,
        domain_user: User,
        test_ulid: ULID,
        test_messenger_record_id: ULID,
        test_datetime: datetime,
    ) -> None:
        mock_session = AsyncMock()
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        def refresh_side_effect(obj: Any) -> None:
            obj.record_id = test_ulid
            obj.created_at = test_datetime
            obj.updated_at = test_datetime
            obj.messenger_record_id = test_messenger_record_id
            obj.user_id = "user123"

        mock_session.refresh = AsyncMock(side_effect=refresh_side_effect)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAUserRepository(mock_session_factory)
        result = await repository.create(domain_user)

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.CREATED
        assert result.response is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_awaited_once()
        mock_session.refresh.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_create_failure(self, domain_user: User) -> None:
        mock_session = AsyncMock()
        mock_session.add = MagicMock(side_effect=Exception("Database error"))

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAUserRepository(mock_session_factory)
        result = await repository.create(domain_user)

        assert result.is_success == RepositoryResultStatusEnum.ERROR
        assert result.status == RepositoryResponseStatusEnum.FAILED
        assert result.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert result.message is not None
        assert "Database error" in result.message


class TestSAUserRepositoryGet:
    @pytest.mark.asyncio
    async def test_get_success_found(self, mock_sa_user: Any, test_ulid: ULID) -> None:
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_sa_user

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAUserRepository(mock_session_factory)
        record_id = UserRecordID(root=test_ulid)
        result = await repository.get(record_id)

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.READ
        assert result.response is not None

    @pytest.mark.asyncio
    async def test_get_success_not_found(self, test_ulid: ULID) -> None:
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAUserRepository(mock_session_factory)
        record_id = UserRecordID(root=test_ulid)
        result = await repository.get(record_id)

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.READ
        assert result.response is None

    @pytest.mark.asyncio
    async def test_get_failure(self, test_ulid: ULID) -> None:
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=Exception("Database error"))

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAUserRepository(mock_session_factory)
        record_id = UserRecordID(root=test_ulid)
        result = await repository.get(record_id)

        assert result.is_success == RepositoryResultStatusEnum.ERROR
        assert result.status == RepositoryResponseStatusEnum.FAILED
        assert result.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert result.message is not None
        assert "Database error" in result.message


class TestSAUserRepositoryGetByUserIdAndMessenger:
    @pytest.mark.asyncio
    async def test_get_by_user_id_and_messenger_success_found(
        self, mock_sa_user: Any, test_messenger_record_id: ULID
    ) -> None:
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_sa_user

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAUserRepository(mock_session_factory)
        user_id = UserID(root="user123")
        messenger_record_id = UserMessengerRecordID(root=test_messenger_record_id)
        result = await repository.get_by_user_id_and_messenger(
            user_id, messenger_record_id
        )

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.READ
        assert result.response is not None

    @pytest.mark.asyncio
    async def test_get_by_user_id_and_messenger_success_not_found(
        self, test_messenger_record_id: ULID
    ) -> None:
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAUserRepository(mock_session_factory)
        user_id = UserID(root="user123")
        messenger_record_id = UserMessengerRecordID(root=test_messenger_record_id)
        result = await repository.get_by_user_id_and_messenger(
            user_id, messenger_record_id
        )

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.READ
        assert result.response is None

    @pytest.mark.asyncio
    async def test_get_by_user_id_and_messenger_failure(
        self, test_messenger_record_id: ULID
    ) -> None:
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=Exception("Database error"))

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAUserRepository(mock_session_factory)
        user_id = UserID(root="user123")
        messenger_record_id = UserMessengerRecordID(root=test_messenger_record_id)
        result = await repository.get_by_user_id_and_messenger(
            user_id, messenger_record_id
        )

        assert result.is_success == RepositoryResultStatusEnum.ERROR
        assert result.status == RepositoryResponseStatusEnum.FAILED
        assert result.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert result.message is not None
        assert "Database error" in result.message


class TestSAUserRepositoryGetOrCreate:
    @pytest.mark.asyncio
    async def test_get_or_create_returns_existing_user(
        self,
        domain_user: User,
        mock_sa_user: Any,
        test_messenger_record_id: ULID,
    ) -> None:
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_sa_user

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAUserRepository(mock_session_factory)
        result = await repository.get_or_create(domain_user)

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.READ
        assert result.response is not None

    @pytest.mark.asyncio
    async def test_get_or_create_creates_new_user(
        self,
        domain_user: User,
        test_ulid: ULID,
        test_messenger_record_id: ULID,
        test_datetime: datetime,
    ) -> None:
        # First call returns None (user not found)
        mock_result_get = MagicMock()
        mock_result_get.scalar_one_or_none.return_value = None

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result_get)
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        def refresh_side_effect(obj: Any) -> None:
            obj.record_id = test_ulid
            obj.created_at = test_datetime
            obj.updated_at = test_datetime
            obj.messenger_record_id = test_messenger_record_id
            obj.user_id = "user123"

        mock_session.refresh = AsyncMock(side_effect=refresh_side_effect)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAUserRepository(mock_session_factory)
        result = await repository.get_or_create(domain_user)

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.CREATED
        assert result.response is not None

    @pytest.mark.asyncio
    async def test_get_or_create_returns_error_on_get_failure(
        self, domain_user: User
    ) -> None:
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=Exception("Database error"))

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAUserRepository(mock_session_factory)
        result = await repository.get_or_create(domain_user)

        assert result.is_success == RepositoryResultStatusEnum.ERROR
        assert result.status == RepositoryResponseStatusEnum.FAILED
        assert result.reason == RepositoryFailedResponseEnum.UNKNOWN
