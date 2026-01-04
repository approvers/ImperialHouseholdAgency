from abc import abstractmethod

from src.system.domain.interface.repository.common.base import RepositoryBase
from src.system.domain.interface.repository.common.response import RepositoryResponse
from src.system.domain.model.user import User
from src.system.domain.value.user import UserRecordID, UserID, UserMessengerRecordID


class UserRepository(RepositoryBase):
    @abstractmethod
    async def create(self, user: User) -> RepositoryResponse[User | None]:
        pass

    @abstractmethod
    async def get(self, record_id: UserRecordID) -> RepositoryResponse[User | None]:
        pass

    @abstractmethod
    async def get_by_user_id_and_messenger(
        self, user_id: UserID, messenger_record_id: UserMessengerRecordID
    ) -> RepositoryResponse[User | None]:
        pass

    @abstractmethod
    async def get_or_create(self, user: User) -> RepositoryResponse[User | None]:
        pass
