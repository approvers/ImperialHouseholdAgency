from datetime import datetime
from typing import Any

import pytest
from ulid import ULID

from src.system.domain.model.nickname import (
    NicknameChangelog as DomainNicknameChangelog,
)
from src.system.domain.value.nickname import (
    NicknameChangelogRecordID,
    NicknameChangelogCreatedAt,
    NicknameChangelogUserRecordID,
    NicknameChangelogBefore,
    NicknameChangelogAfter,
)
from src.system.infrastructure.repository.sqlalchemy.model.all import load_all_sa_models
from src.system.infrastructure.repository.sqlalchemy.model.nickname import (
    NicknameChangelog as SANicknameChangelog,
)
from src.system.infrastructure.repository.sqlalchemy.translator.nickname import (
    SANicknameChangelogTranslator,
)
from src.system.util.id import generate_ulid


@pytest.fixture
def test_ulid() -> ULID:
    return generate_ulid()


@pytest.fixture
def test_datetime() -> datetime:
    return datetime(2023, 1, 1, 12, 0, 0)


@pytest.fixture
def test_user_record_id() -> ULID:
    return generate_ulid()


@pytest.fixture
def test_before() -> str:
    return "old_nickname"


@pytest.fixture
def test_after() -> str:
    return "new_nickname"


class DBRecord:
    def __init__(
        self,
        record_id: ULID,
        created_at: datetime,
        user_record_id: ULID,
        before: str,
        after: str,
    ) -> None:
        self.record_id = record_id
        self.created_at = created_at
        self.user_record_id = user_record_id
        self.before = before
        self.after = after


@pytest.fixture
def db_record(
    test_ulid: ULID,
    test_datetime: datetime,
    test_user_record_id: ULID,
    test_before: str,
    test_after: str,
) -> Any:
    return DBRecord(
        record_id=test_ulid,
        created_at=test_datetime,
        user_record_id=test_user_record_id,
        before=test_before,
        after=test_after,
    )


@pytest.fixture
def domain_model(
    test_ulid: ULID,
    test_datetime: datetime,
    test_user_record_id: ULID,
    test_before: str,
    test_after: str,
) -> DomainNicknameChangelog:
    # noinspection PyArgumentList
    return DomainNicknameChangelog(
        record_id=NicknameChangelogRecordID(root=test_ulid),
        created_at=NicknameChangelogCreatedAt(root=test_datetime),
        user_record_id=NicknameChangelogUserRecordID(root=test_user_record_id),
        before=NicknameChangelogBefore(root=test_before),
        after=NicknameChangelogAfter(root=test_after),
    )


def test_to_domain(
    db_record: Any,
    test_ulid: ULID,
    test_datetime: datetime,
    test_user_record_id: ULID,
    test_before: str,
    test_after: str,
) -> None:
    result = SANicknameChangelogTranslator.to_domain(db_record)

    assert isinstance(result, DomainNicknameChangelog)
    assert result.record_id == NicknameChangelogRecordID(root=test_ulid)
    assert result.created_at == NicknameChangelogCreatedAt(root=test_datetime)
    assert result.user_record_id == NicknameChangelogUserRecordID(
        root=test_user_record_id
    )
    # noinspection PyArgumentList
    assert result.before == NicknameChangelogBefore(root=test_before)
    # noinspection PyArgumentList
    assert result.after == NicknameChangelogAfter(root=test_after)


# noinspection DuplicatedCode
def test_to_db_record(
    domain_model: DomainNicknameChangelog,
    test_ulid: ULID,
    test_datetime: datetime,
    test_user_record_id: ULID,
    test_before: str,
    test_after: str,
) -> None:
    load_all_sa_models()

    result = SANicknameChangelogTranslator.to_db_record(domain_model)

    assert isinstance(result, SANicknameChangelog)
    assert result.record_id == test_ulid
    assert result.created_at == test_datetime
    assert result.user_record_id == test_user_record_id
    assert result.before == test_before
    assert result.after == test_after
