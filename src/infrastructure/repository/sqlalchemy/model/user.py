from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ulid import ULID

from src.infrastructure.repository.sqlalchemy.model.baes import (
    Base,
    ULIDMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
)
from src.infrastructure.repository.sqlalchemy.type.ulid import ULIDColumn

if TYPE_CHECKING:
    # noinspection PyUnusedImports
    from src.infrastructure.repository.sqlalchemy.model.messenger import Messenger


class User(ULIDMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("messenger_id", "user_id"),)

    messenger_id: Mapped[ULID] = mapped_column(
        ULIDColumn(),
        ForeignKey("messenger.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(String(), nullable=False)

    messenger: Mapped["Messenger"] = relationship("Messenger")
