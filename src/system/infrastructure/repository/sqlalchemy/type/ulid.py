from sqlalchemy import String, TypeDecorator, Dialect
from ulid import ULID


class ULIDColumn(TypeDecorator[ULID]):
    impl: String = String(length=26)
    cache_ok = True

    def process_bind_param(self, value: ULID | None, dialect: Dialect) -> str | None:
        if value is not None:
            return str(value)

        return value

    def process_result_value(self, value: str | None, dialect: Dialect) -> ULID | None:
        if value is not None:
            return ULID.from_str(value)

        return value
