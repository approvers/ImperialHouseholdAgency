import datetime

from ulid import ULID

from src.system.util.datetime import utcnow


def generate_ulid(value: datetime.datetime | None = None) -> ULID:
    value = value or utcnow()

    return ULID.from_datetime(value)
