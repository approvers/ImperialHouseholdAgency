from datetime import datetime
from typing import Any

import pytest
from ulid import ULID

from src.domain.model.messenger import Messenger as DomainMessenger
from src.domain.value.messenger import (
    MessengerRecordID,
    MessengerCreatedAt,
    MessengerUpdatedAt,
    MessengerName,
)
from src.infrastructure.repository.sqlalchemy.model.all import load_all_sa_models
from src.infrastructure.repository.sqlalchemy.model.messenger import (
    Messenger as SAMessenger,
)
from src.infrastructure.repository.sqlalchemy.translator.messenger import (
    SAMessengerTranslator,
)
from src.util.id import generate_ulid


@pytest.fixture
def test_ulid() -> ULID:
    return generate_ulid()


@pytest.fixture
def test_datetime() -> datetime:
    return datetime(2023, 1, 1, 12, 0, 0)


@pytest.fixture
def test_name() -> str:
    return "test_messenger"


@pytest.fixture
def db_record(test_ulid: ULID, test_datetime: datetime, test_name: str) -> Any:
    # Create a simple object with required attributes instead of using SQLAlchemy model
    class MockDBRecord:
        def __init__(self) -> None:
            self.record_id = test_ulid
            self.created_at = test_datetime
            self.updated_at = test_datetime
            self.name = test_name

    return MockDBRecord()


@pytest.fixture
def domain_model(
    test_ulid: ULID, test_datetime: datetime, test_name: str
) -> DomainMessenger:
    # noinspection PyArgumentList
    return DomainMessenger(
        record_id=MessengerRecordID(root=test_ulid),
        created_at=MessengerCreatedAt(root=test_datetime),
        updated_at=MessengerUpdatedAt(root=test_datetime),
        name=MessengerName(root=test_name),
    )


def test_to_domain(
    db_record: Any, test_ulid: ULID, test_datetime: datetime, test_name: str
) -> None:
    result = SAMessengerTranslator.to_domain(db_record)

    assert isinstance(result, DomainMessenger)
    assert result.record_id == MessengerRecordID(root=test_ulid)
    assert result.created_at == MessengerCreatedAt(root=test_datetime)
    assert result.updated_at == MessengerUpdatedAt(root=test_datetime)
    # noinspection PyArgumentList
    assert result.name == MessengerName(root=test_name)


def test_to_db_record(
    domain_model: DomainMessenger,
    test_ulid: ULID,
    test_datetime: datetime,
    test_name: str,
    monkeypatch: Any,
) -> None:
    load_all_sa_models()

    result = SAMessengerTranslator.to_db_record(domain_model)

    assert isinstance(result, SAMessenger)
    assert result.record_id == test_ulid
    assert result.created_at == test_datetime
    assert result.updated_at == test_datetime
