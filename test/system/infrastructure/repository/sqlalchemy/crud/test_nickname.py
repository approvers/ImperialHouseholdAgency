from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from ulid import ULID

from src.system.domain.interface.repository.common.option import SortOrder
from src.system.domain.interface.repository.common.response import (
    RepositoryResultStatusEnum,
    RepositoryResponseStatusEnum,
    RepositoryFailedResponseEnum,
)
from src.system.domain.model.nickname import NicknameChangelog
from src.system.domain.value.nickname import (
    NicknameChangelogRecordID,
    NicknameChangelogCreatedAt,
    NicknameChangelogUserRecordID,
    NicknameChangelogBefore,
    NicknameChangelogAfter,
)
from src.system.infrastructure.repository.sqlalchemy.crud.nickname import (
    SANicknameChangelogRepository,
)
from src.system.util.id import generate_ulid


@pytest.fixture
def test_ulid() -> ULID:
    return generate_ulid()


@pytest.fixture
def test_user_record_id() -> ULID:
    return generate_ulid()


@pytest.fixture
def test_datetime() -> datetime:
    return datetime(2023, 1, 1, 12, 0, 0)


@pytest.fixture
def domain_nickname_changelog(
    test_ulid: ULID, test_user_record_id: ULID, test_datetime: datetime
) -> NicknameChangelog:
    return NicknameChangelog(
        record_id=NicknameChangelogRecordID(root=test_ulid),
        created_at=NicknameChangelogCreatedAt(root=test_datetime),
        user_record_id=NicknameChangelogUserRecordID(root=test_user_record_id),
        before=NicknameChangelogBefore(root="old_name"),
        after=NicknameChangelogAfter(root="new_name"),
    )


@pytest.fixture
def mock_sa_nickname_changelog(
    test_ulid: ULID, test_user_record_id: ULID, test_datetime: datetime
) -> Any:
    mock = MagicMock()
    mock.record_id = test_ulid
    mock.created_at = test_datetime
    mock.user_record_id = test_user_record_id
    mock.before = "old_name"
    mock.after = "new_name"
    return mock


class TestSANicknameChangelogRepositoryCreate:
    @pytest.mark.asyncio
    async def test_create_success(
        self,
        domain_nickname_changelog: NicknameChangelog,
        test_ulid: ULID,
        test_user_record_id: ULID,
        test_datetime: datetime,
    ) -> None:
        mock_session = AsyncMock()
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock(
            side_effect=lambda obj: setattr(obj, "record_id", test_ulid)
            or setattr(obj, "created_at", test_datetime)
            or setattr(obj, "user_record_id", test_user_record_id)
            or setattr(obj, "before", "old_name")
            or setattr(obj, "after", "new_name")
        )

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SANicknameChangelogRepository(mock_session_factory)
        result = await repository.create(domain_nickname_changelog)

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.CREATED
        assert result.response is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_awaited_once()
        mock_session.refresh.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_create_failure(
        self, domain_nickname_changelog: NicknameChangelog
    ) -> None:
        mock_session = AsyncMock()
        mock_session.add = MagicMock(side_effect=Exception("Database error"))

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SANicknameChangelogRepository(mock_session_factory)
        result = await repository.create(domain_nickname_changelog)

        assert result.is_success == RepositoryResultStatusEnum.ERROR
        assert result.status == RepositoryResponseStatusEnum.FAILED
        assert result.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert result.message is not None
        assert "Database error" in result.message


class TestSANicknameChangelogRepositoryGetByUserRecordId:
    @pytest.mark.asyncio
    async def test_get_by_user_record_id_success_asc(
        self, mock_sa_nickname_changelog: Any, test_user_record_id: ULID
    ) -> None:
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_sa_nickname_changelog]

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SANicknameChangelogRepository(mock_session_factory)
        user_record_id = NicknameChangelogUserRecordID(root=test_user_record_id)
        result = await repository.get_by_user_record_id(
            user_record_id, SortOrder.ASC, 10
        )

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.READ
        assert len(list(result.response)) == 1

    @pytest.mark.asyncio
    async def test_get_by_user_record_id_success_desc(
        self, mock_sa_nickname_changelog: Any, test_user_record_id: ULID
    ) -> None:
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_sa_nickname_changelog]

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SANicknameChangelogRepository(mock_session_factory)
        user_record_id = NicknameChangelogUserRecordID(root=test_user_record_id)
        result = await repository.get_by_user_record_id(
            user_record_id, SortOrder.DESC, 10
        )

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.READ
        assert len(list(result.response)) == 1

    @pytest.mark.asyncio
    async def test_get_by_user_record_id_success_empty(
        self, test_user_record_id: ULID
    ) -> None:
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SANicknameChangelogRepository(mock_session_factory)
        user_record_id = NicknameChangelogUserRecordID(root=test_user_record_id)
        result = await repository.get_by_user_record_id(
            user_record_id, SortOrder.DESC, 10
        )

        assert result.is_success == RepositoryResultStatusEnum.SUCCESS
        assert result.status == RepositoryResponseStatusEnum.READ
        assert len(list(result.response)) == 0

    @pytest.mark.asyncio
    async def test_get_by_user_record_id_failure(
        self, test_user_record_id: ULID
    ) -> None:
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=Exception("Database error"))

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(
            return_value=mock_session
        )
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        repository = SANicknameChangelogRepository(mock_session_factory)
        user_record_id = NicknameChangelogUserRecordID(root=test_user_record_id)
        result = await repository.get_by_user_record_id(
            user_record_id, SortOrder.ASC, 10
        )

        assert result.is_success == RepositoryResultStatusEnum.ERROR
        assert result.status == RepositoryResponseStatusEnum.FAILED
        assert result.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert result.message is not None
        assert "Database error" in result.message
