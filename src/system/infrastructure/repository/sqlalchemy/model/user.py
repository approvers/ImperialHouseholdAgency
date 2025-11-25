from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ulid import ULID

from src.system.infrastructure.repository.sqlalchemy.model.base import (
    Base,
    ULIDMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
)
from src.system.infrastructure.repository.sqlalchemy.type.ulid import ULIDColumn

if TYPE_CHECKING:
    # noinspection PyUnusedImports
    from src.system.infrastructure.repository.sqlalchemy.model.messenger import (
        Messenger,
    )

    # noinspection PyUnusedImports
    from src.system.infrastructure.repository.sqlalchemy.model.nickname import (
        NicknameChangelog,
    )


class User(ULIDMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("messenger_record_id", "user_id"),)

    messenger_record_id: Mapped[ULID] = mapped_column(
        ULIDColumn(),
        ForeignKey("messenger.record_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(String(), nullable=False)

    # Forward populates
    messenger: Mapped["Messenger"] = relationship(
        "Messenger", back_populates="users", foreign_keys=[messenger_record_id]
    )

    # Back populates
    nickname_changelogs: Mapped[list["NicknameChangelog"]] = relationship(
        "NicknameChangelog",
        back_populates="user",
    )
