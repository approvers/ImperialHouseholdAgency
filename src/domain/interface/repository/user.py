from abc import abstractmethod

from src.domain.interface.repository.common.base import RepositoryBase
from src.domain.interface.repository.common.response import RepositoryResponse
from src.domain.model.user import User
from src.domain.value.user import UserRecordID


class UserRepository(RepositoryBase):
    @abstractmethod
    async def create(self, user: User) -> RepositoryResponse[User | None]:
        pass

    @abstractmethod
    async def get(self, record_id: UserRecordID) -> RepositoryResponse[User | None]:
        pass

    async def get_or_create(self, user: User) -> RepositoryResponse[User | None]:
        existing = await self.get(user.record_id)

        if existing.response:
            return existing

        created = await self.create(user)

        return created
