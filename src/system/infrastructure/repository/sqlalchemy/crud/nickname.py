from typing import Iterable

import logfire
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.system.domain.interface.repository.common.option import SortOrder
from src.system.domain.interface.repository.common.response import (
    RepositoryResponse,
    RepositoryResultStatusEnum,
    RepositoryResponseStatusEnum,
    RepositoryFailedResponseEnum,
)
from src.system.domain.interface.repository.nickname import NicknameChangelogRepository
from src.system.domain.model.nickname import NicknameChangelog
from src.system.domain.value.nickname import NicknameChangelogUserRecordID
from src.system.infrastructure.repository.sqlalchemy.model.nickname import (
    NicknameChangelog as SANicknameChangelog,
)
from src.system.infrastructure.repository.sqlalchemy.translator.nickname import (
    SANicknameChangelogTranslator,
)


class SANicknameChangelogRepository(NicknameChangelogRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    @logfire.instrument(span_name="SANicknameChangelogRepository.create()")
    async def create(
        self, data: NicknameChangelog
    ) -> RepositoryResponse[NicknameChangelog | None]:
        try:
            async with self.session_factory() as session:
                sa_nickname_changelog = SANicknameChangelogTranslator.to_db_record(data)

                session.add(sa_nickname_changelog)
                await session.commit()
                await session.refresh(sa_nickname_changelog)

                created_nickname_changelog = SANicknameChangelogTranslator.to_domain(
                    sa_nickname_changelog
                )

                return RepositoryResponse[NicknameChangelog | None](
                    response=created_nickname_changelog,
                    is_success=RepositoryResultStatusEnum.SUCCESS,
                    status=RepositoryResponseStatusEnum.CREATED,
                )

        except Exception as e:
            return RepositoryResponse[NicknameChangelog | None](
                response=data,
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
                reason=RepositoryFailedResponseEnum.UNKNOWN,
                message=f"Failed to create nickname changelog: {str(e)}",
            )

    @logfire.instrument(
        span_name="SANicknameChangelogRepository.get_by_user_record_id()"
    )
    async def get_by_user_record_id(
        self,
        user_record_id: NicknameChangelogUserRecordID,
        sort_order: SortOrder,
        limit: int,
    ) -> RepositoryResponse[Iterable[NicknameChangelog]]:
        try:
            async with self.session_factory() as session:
                order_by_column = (
                    SANicknameChangelog.created_at.asc()
                    if sort_order == SortOrder.ASC
                    else SANicknameChangelog.created_at.desc()
                )

                stmt = (
                    select(SANicknameChangelog)
                    .where(SANicknameChangelog.user_record_id == user_record_id.root)
                    .order_by(order_by_column)
                    .limit(limit)
                )
                result = await session.execute(stmt)
                sa_nickname_changelogs = result.scalars().all()

                domain_nickname_changelogs = [
                    SANicknameChangelogTranslator.to_domain(sa_nickname_changelog)
                    for sa_nickname_changelog in sa_nickname_changelogs
                ]

                return RepositoryResponse[Iterable[NicknameChangelog]](
                    response=domain_nickname_changelogs,
                    is_success=RepositoryResultStatusEnum.SUCCESS,
                    status=RepositoryResponseStatusEnum.READ,
                )

        except Exception as e:
            return RepositoryResponse[Iterable[NicknameChangelog]](
                response=[],
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
                reason=RepositoryFailedResponseEnum.UNKNOWN,
                message=f"Failed to retrieve nickname changelogs by user_record_id: {str(e)}",
            )
