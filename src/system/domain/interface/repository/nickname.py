from abc import abstractmethod
from typing import Iterable

from src.system.domain.interface.repository.common.base import RepositoryBase
from src.system.domain.interface.repository.common.option import SortOrder
from src.system.domain.interface.repository.common.response import RepositoryResponse
from src.system.domain.model.nickname import NicknameChangelog
from src.system.domain.value.nickname import NicknameChangelogUserRecordID


class NicknameChangelogRepository(RepositoryBase):
    @abstractmethod
    async def create(
        self, data: NicknameChangelog
    ) -> RepositoryResponse[NicknameChangelog | None]:
        pass

    @abstractmethod
    async def get_by_user_record_id(
        self,
        user_record_id: NicknameChangelogUserRecordID,
        sort_order: SortOrder,
        limit: int,
    ) -> RepositoryResponse[Iterable[NicknameChangelog]]:
        pass
