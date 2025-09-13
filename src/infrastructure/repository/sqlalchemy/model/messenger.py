from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.repository.sqlalchemy.model.baes import (
    Base,
    ULIDMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
)


class Messenger(ULIDMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "messenger"

    name: Mapped[str] = mapped_column(String(), nullable=False)
