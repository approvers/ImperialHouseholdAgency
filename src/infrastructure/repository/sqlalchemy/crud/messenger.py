from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.domain.interface.repository.common.response import (
    RepositoryResponse,
    RepositoryResultStatusEnum,
    RepositoryResponseStatusEnum,
    RepositoryFailedResponseEnum,
)
from src.domain.interface.repository.messenger import MessengerRepository
from src.domain.model.messenger import Messenger
from src.infrastructure.repository.sqlalchemy.model.messenger import (
    Messenger as SAMessenger,
)
from src.infrastructure.repository.sqlalchemy.translator.messenger import (
    SAMessengerTranslator,
)


class SAMessengerRepository(MessengerRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def create(self, data: Messenger) -> RepositoryResponse[Messenger | None]:
        try:
            async with self.session_factory() as session:
                sa_messenger = SAMessengerTranslator.to_db_record(data)

                session.add(sa_messenger)
                await session.commit()
                await session.refresh(sa_messenger)

                created_messenger = SAMessengerTranslator.to_domain(sa_messenger)

                return RepositoryResponse[Messenger | None](
                    response=created_messenger,
                    is_success=RepositoryResultStatusEnum.SUCCESS,
                    status=RepositoryResponseStatusEnum.CREATED,
                )

        except Exception as e:
            return RepositoryResponse[Messenger | None](
                response=data,
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
                reason=RepositoryFailedResponseEnum.UNKNOWN,
                message=f"Failed to create messenger: {str(e)}",
            )

    async def get_all(self) -> RepositoryResponse[Iterable[Messenger]]:
        try:
            async with self.session_factory() as session:
                stmt = select(SAMessenger)
                result = await session.execute(stmt)
                sa_messengers = result.scalars().all()

                domain_messengers = [
                    SAMessengerTranslator.to_domain(sa_messenger)
                    for sa_messenger in sa_messengers
                ]

                return RepositoryResponse[Iterable[Messenger]](
                    response=domain_messengers,
                    is_success=RepositoryResultStatusEnum.SUCCESS,
                    status=RepositoryResponseStatusEnum.READ,
                )

        except Exception as e:
            return RepositoryResponse[Iterable[Messenger]](
                response=[],
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
                reason=RepositoryFailedResponseEnum.UNKNOWN,
                message=f"Failed to retrieve messengers: {str(e)}",
            )
