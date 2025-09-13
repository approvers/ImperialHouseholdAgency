from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.repository.sqlalchemy.model.base import (
    Base,
    ULIDMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
)

if TYPE_CHECKING:
    # noinspection PyUnusedImports
    from src.infrastructure.repository.sqlalchemy.model.user import User


class Messenger(ULIDMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "messenger"

    # Real columns
    name: Mapped[str] = mapped_column(String(), nullable=False)

    # Back populates
    users: Mapped[list["User"]] = relationship("User", back_populates="messenger")
