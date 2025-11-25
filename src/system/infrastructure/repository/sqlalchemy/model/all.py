from typing import Final

from src.system.infrastructure.repository.sqlalchemy.model.base import Base
from src.system.infrastructure.repository.sqlalchemy.model.messenger import Messenger
from src.system.infrastructure.repository.sqlalchemy.model.nickname import (
    NicknameChangelog,
)
from src.system.infrastructure.repository.sqlalchemy.model.user import User

MODELS: Final[tuple[type[Base], ...]] = (Messenger, User, NicknameChangelog)


def load_all_sa_models() -> None:
    pass
