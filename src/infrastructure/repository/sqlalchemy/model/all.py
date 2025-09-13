from typing import Final

from src.infrastructure.repository.sqlalchemy.model.baes import Base
from src.infrastructure.repository.sqlalchemy.model.messenger import Messenger
from src.infrastructure.repository.sqlalchemy.model.nickname import NicknameChangelog
from src.infrastructure.repository.sqlalchemy.model.user import User

MODELS: Final[tuple[type[Base], ...]] = (Messenger, User, NicknameChangelog)
