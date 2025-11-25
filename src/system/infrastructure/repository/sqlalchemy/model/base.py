from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from ulid import ULID

from src.system.infrastructure.repository.sqlalchemy.type.ulid import ULIDColumn
from src.system.util.datetime import utcnow
from src.system.util.id import generate_ulid


class Base(DeclarativeBase):
    pass


class ULIDMixin:
    record_id: Mapped[ULID] = mapped_column(
        ULIDColumn(), primary_key=True, default=generate_ulid
    )


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utcnow
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utcnow
    )
