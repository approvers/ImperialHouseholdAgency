from datetime import datetime
from typing import Any

import pytest
from ulid import ULID

from src.system.domain.model.user import User as DomainUser
from src.system.domain.value.user import (
    UserRecordID,
    UserCreatedAt,
    UserUpdatedAt,
    UserMessengerRecordID,
    UserID,
)
from src.system.infrastructure.repository.sqlalchemy.model.all import load_all_sa_models
from src.system.infrastructure.repository.sqlalchemy.model.user import User as SAUser
from src.system.infrastructure.repository.sqlalchemy.translator.user import (
    SAUserTranslator,
)
from src.system.util.id import generate_ulid


@pytest.fixture
def test_ulid() -> ULID:
    return generate_ulid()


@pytest.fixture
def test_datetime() -> datetime:
    return datetime(2023, 1, 1, 12, 0, 0)


@pytest.fixture
def test_messenger_record_id() -> ULID:
    return generate_ulid()


@pytest.fixture
def test_user_id() -> str:
    return "test_user_123"


class DBRecord:
    def __init__(
        self,
        record_id: ULID,
        created_at: datetime,
        updated_at: datetime,
        messenger_record_id: ULID,
        user_id: str,
    ) -> None:
        self.record_id = record_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.messenger_record_id = messenger_record_id
        self.user_id = user_id


@pytest.fixture
def db_record(
    test_ulid: ULID,
    test_datetime: datetime,
    test_messenger_record_id: ULID,
    test_user_id: str,
) -> Any:
    return DBRecord(
        record_id=test_ulid,
        created_at=test_datetime,
        updated_at=test_datetime,
        messenger_record_id=test_messenger_record_id,
        user_id=test_user_id,
    )


@pytest.fixture
def domain_model(
    test_ulid: ULID,
    test_datetime: datetime,
    test_messenger_record_id: ULID,
    test_user_id: str,
) -> DomainUser:
    # noinspection PyArgumentList
    return DomainUser(
        record_id=UserRecordID(root=test_ulid),
        created_at=UserCreatedAt(root=test_datetime),
        updated_at=UserUpdatedAt(root=test_datetime),
        messenger_record_id=UserMessengerRecordID(root=test_messenger_record_id),
        id=UserID(root=test_user_id),
    )


def test_to_domain(
    db_record: Any,
    test_ulid: ULID,
    test_datetime: datetime,
    test_messenger_record_id: ULID,
    test_user_id: str,
) -> None:
    result = SAUserTranslator.to_domain(db_record)

    assert isinstance(result, DomainUser)
    assert result.record_id == UserRecordID(root=test_ulid)
    assert result.created_at == UserCreatedAt(root=test_datetime)
    assert result.updated_at == UserUpdatedAt(root=test_datetime)
    assert result.messenger_record_id == UserMessengerRecordID(
        root=test_messenger_record_id
    )
    # noinspection PyArgumentList
    assert result.id == UserID(root=test_user_id)


# noinspection DuplicatedCode
def test_to_db_record(
    domain_model: DomainUser,
    test_ulid: ULID,
    test_datetime: datetime,
    test_messenger_record_id: ULID,
    test_user_id: str,
) -> None:
    load_all_sa_models()

    result = SAUserTranslator.to_db_record(domain_model)

    assert isinstance(result, SAUser)
    assert result.record_id == test_ulid
    assert result.created_at == test_datetime
    assert result.updated_at == test_datetime
    assert result.messenger_record_id == test_messenger_record_id
    assert result.user_id == test_user_id
