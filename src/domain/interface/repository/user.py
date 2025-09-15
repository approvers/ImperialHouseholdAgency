from abc import abstractmethod

from src.domain.interface.repository.common.base import RepositoryBase
from src.domain.interface.repository.common.response import RepositoryResponse
from src.domain.interface.repository.common.session import SessionIF
from src.domain.model.user import User
from src.domain.value.user import UserRecordID, UserID, UserMessengerRecordID


class UserRepository(RepositoryBase):
    @abstractmethod
    async def create(
        self, user: User, session: SessionIF
    ) -> RepositoryResponse[User | None]:
        pass

    @abstractmethod
    async def get(
        self, record_id: UserRecordID, session: SessionIF
    ) -> RepositoryResponse[User | None]:
        pass

    @abstractmethod
    async def get_by_user_id(
        self,
        messenger_record_id: UserMessengerRecordID,
        user_id: UserID,
        session: SessionIF,
    ) -> RepositoryResponse[User | None]:
        pass

    async def get_or_create(
        self, user: User, session: SessionIF
    ) -> RepositoryResponse[User | None]:
        existing = await self.get_by_user_id(user.messenger_record_id, user.id, session)

        if existing.response:
            return existing

        created = await self.create(user, session)

        return created
