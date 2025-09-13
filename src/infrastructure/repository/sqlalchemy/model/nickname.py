from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.repository.sqlalchemy.model.baes import (
    Base,
    ULIDMixin,
    CreatedAtMixin,
)

if TYPE_CHECKING:
    # noinspection PyUnusedImports
    from src.infrastructure.repository.sqlalchemy.model.user import User


class NicknameChangelog(ULIDMixin, CreatedAtMixin, Base):
    __tablename__ = "nickname_changelog"

    # Real columns
    user_id: Mapped[str] = mapped_column(String(), nullable=False)
    before: Mapped[str] = mapped_column(String(), nullable=True)
    after: Mapped[str] = mapped_column(String(), nullable=False)

    # Forward populates
    user: Mapped["User"] = relationship(
        "User", back_populates="nickname_changelogs", foreign_keys=[user_id]
    )
