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
from src.system.domain.model.messenger import Messenger
from src.system.domain.value.messenger import (
    MessengerRecordID,
    MessengerCreatedAt,
    MessengerUpdatedAt,
    MessengerName,
)
from src.system.infrastructure.repository.sqlalchemy.crud.messenger import (
    SAMessengerRepository,
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
        name=MessengerName(root="test_messenger"),
    )


@pytest.fixture
def mock_sa_messenger(test_ulid: ULID, test_datetime: datetime) -> Any:
    mock = MagicMock()
    mock.record_id = test_ulid
    mock.created_at = test_datetime
    mock.updated_at = test_datetime
    mock.name = "test_messenger"
    return mock


class TestSAMessengerRepositoryCreate:
    @pytest.mark.asyncio
    async def test_create_success(
        self,
        domain_messenger: Messenger,
        mock_sa_messenger: Any,
        test_ulid: ULID,
        test_datetime: datetime,
    ) -> None:
        mock_session = AsyncMock()
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        def refresh_side_effect(obj: Any) -> None:
            obj.record_id = test_ulid
            obj.created_at = test_datetime
            obj.updated_at = test_datetime
            obj.name = "test_messenger"

        mock_session.refresh = AsyncMock(side_effect=refresh_side_effect)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAMessengerRepository(mock_session_factory)
        result = await repository.create(domain_messenger)

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.CREATED
        assert result.response is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_awaited_once()
        mock_session.refresh.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_create_failure(self, domain_messenger: Messenger) -> None:
        mock_session = AsyncMock()
        mock_session.add = MagicMock(side_effect=Exception("Database error"))

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAMessengerRepository(mock_session_factory)
        result = await repository.create(domain_messenger)

        assert result.is_success == RepositoryResultStatusEnum.ERROR
        assert result.status == RepositoryResponseStatusEnum.FAILED
        assert result.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert result.message is not None
        assert "Database error" in result.message


class TestSAMessengerRepositoryGetAll:
    @pytest.mark.asyncio
    async def test_get_all_success_with_results(self, mock_sa_messenger: Any) -> None:
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_sa_messenger]

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAMessengerRepository(mock_session_factory)
        result = await repository.get_all()

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.READ
        assert len(list(result.response)) == 1

    @pytest.mark.asyncio
    async def test_get_all_success_empty(self) -> None:
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAMessengerRepository(mock_session_factory)
        result = await repository.get_all()

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.READ
        assert len(list(result.response)) == 0

    @pytest.mark.asyncio
    async def test_get_all_failure(self) -> None:
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=Exception("Database error"))

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SAMessengerRepository(mock_session_factory)
        result = await repository.get_all()

        assert result.is_success == RepositoryResultStatusEnum.ERROR
        assert result.status == RepositoryResponseStatusEnum.FAILED
        assert result.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert result.message is not None
        assert "Database error" in result.message
