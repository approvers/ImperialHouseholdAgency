from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ulid import ULID

from src.infrastructure.repository.sqlalchemy.model.base import (
    Base,
    ULIDMixin,
    CreatedAtMixin,
)
from src.infrastructure.repository.sqlalchemy.type.ulid import ULIDColumn

if TYPE_CHECKING:
    # noinspection PyUnusedImports
    from src.infrastructure.repository.sqlalchemy.model.user import User


class NicknameChangelog(ULIDMixin, CreatedAtMixin, Base):
    __tablename__ = "nickname_changelog"

    # Real columns
    user_record_id: Mapped[ULID] = mapped_column(
        ULIDColumn(), ForeignKey("user.record_id"), nullable=False
    )
    before: Mapped[str] = mapped_column(String(), nullable=True)
    after: Mapped[str] = mapped_column(String(), nullable=False)

    # Forward populates
    user: Mapped["User"] = relationship(
        "User", back_populates="nickname_changelogs", foreign_keys=[user_record_id]
    )
