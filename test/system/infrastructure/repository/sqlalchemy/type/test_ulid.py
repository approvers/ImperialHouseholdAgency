from ulid import ULID

from src.system.infrastructure.repository.sqlalchemy.type.ulid import ULIDColumn


def test_ulid_column_init() -> None:
    column = ULIDColumn()
    assert column.cache_ok is True
    assert column.impl.length == 26


def test_process_bind_param_with_ulid(sample_ulid: ULID, dialect: object) -> None:
    column = ULIDColumn()
    result = column.process_bind_param(sample_ulid, dialect)  # type: ignore[arg-type]

    assert result == str(sample_ulid)
    assert isinstance(result, str)


def test_process_bind_param_with_none(dialect: object) -> None:
    column = ULIDColumn()
    result = column.process_bind_param(None, dialect)  # type: ignore[arg-type]

    assert result is None


def test_process_result_value_with_string(
    sample_ulid_str: str, dialect: object
) -> None:
    column = ULIDColumn()
    result = column.process_result_value(sample_ulid_str, dialect)  # type: ignore[arg-type]

    assert isinstance(result, ULID)
    assert str(result) == sample_ulid_str


def test_process_result_value_with_none(dialect: object) -> None:
    column = ULIDColumn()
    result = column.process_result_value(None, dialect)  # type: ignore[arg-type]

    assert result is None


def test_process_bind_param_roundtrip(sample_ulid: ULID, dialect: object) -> None:
    column = ULIDColumn()

    # Convert ULID to string (bind)
    bound_value = column.process_bind_param(sample_ulid, dialect)  # type: ignore[arg-type]
    # Convert string back to ULID (result)
    result_value = column.process_result_value(bound_value, dialect)  # type: ignore[arg-type]

    assert result_value == sample_ulid
