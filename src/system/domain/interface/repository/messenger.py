from abc import abstractmethod
from typing import Iterable

from src.system.domain.interface.repository.common.base import RepositoryBase
from src.system.domain.interface.repository.common.response import RepositoryResponse
from src.system.domain.model.messenger import Messenger
from src.system.domain.value.messenger import MessengerName


class MessengerRepository(RepositoryBase):
    @abstractmethod
    async def create(self, data: Messenger) -> RepositoryResponse[Messenger | None]:
        pass  # pragma: no cover

    @abstractmethod
    async def get_all(self) -> RepositoryResponse[Iterable[Messenger]]:
        pass  # pragma: no cover

    @abstractmethod
    async def get_by_name(
        self, name: MessengerName
    ) -> RepositoryResponse[Messenger | None]:
        pass  # pragma: no cover
