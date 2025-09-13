from typing import Final

from src.infrastructure.repository.sqlalchemy.model.baes import Base
from src.infrastructure.repository.sqlalchemy.model.messenger import Messenger

MODELS: Final[tuple[type[Base]]] = (Messenger,)
