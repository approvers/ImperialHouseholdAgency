from abc import abstractmethod
from typing import Iterable

from src.domain.interface.repository.common.base import RepositoryBase
from src.domain.interface.repository.common.response import RepositoryResponse
from src.domain.model.messenger import Messenger


class MessengerRepository(RepositoryBase):
    @abstractmethod
    async def create(self, data: Messenger) -> RepositoryResponse[Messenger | None]:
        pass

    @abstractmethod
    async def get_all(self) -> RepositoryResponse[Iterable[Messenger]]:
        pass
