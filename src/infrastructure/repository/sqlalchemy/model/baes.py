from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from ulid import ULID

from src.infrastructure.repository.sqlalchemy.type.ulid import ULIDColumn


class Base(DeclarativeBase):
    pass


class ULIDMixin:
    id: Mapped[ULID] = mapped_column(ULIDColumn(), primary_key=True)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
