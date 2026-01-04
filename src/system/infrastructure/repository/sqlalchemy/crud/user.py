import logfire
from injector import inject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.system.domain.interface.repository.common.response import (
    RepositoryResponse,
    RepositoryResultStatusEnum,
    RepositoryResponseStatusEnum,
    RepositoryFailedResponseEnum,
)
from src.system.domain.interface.repository.user import UserRepository
from src.system.domain.model.user import User
from src.system.domain.value.user import UserRecordID, UserID, UserMessengerRecordID
from src.system.infrastructure.repository.sqlalchemy.model.user import User as SAUser
from src.system.infrastructure.repository.sqlalchemy.translator.user import (
    SAUserTranslator,
)


class SAUserRepository(UserRepository):
    @inject
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    @logfire.instrument(span_name="SAUserRepository.create()")
    async def create(self, user: User) -> RepositoryResponse[User | None]:
        try:
            async with self.session_factory() as session:
                sa_user = SAUserTranslator.to_db_record(user)

                session.add(sa_user)
                await session.commit()
                await session.refresh(sa_user)

                created_user = SAUserTranslator.to_domain(sa_user)

                return RepositoryResponse[User | None](
                    response=created_user,
                    is_success=RepositoryResultStatusEnum.SUCCESS,
                    status=RepositoryResponseStatusEnum.CREATED,
                )

        except Exception as e:
            return RepositoryResponse[User | None](
                response=user,
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
                reason=RepositoryFailedResponseEnum.UNKNOWN,
                message=f"Failed to create user: {str(e)}",
            )

    @logfire.instrument(span_name="SAUserRepository.get()")
    async def get(self, record_id: UserRecordID) -> RepositoryResponse[User | None]:
        try:
            async with self.session_factory() as session:
                stmt = select(SAUser).where(SAUser.record_id == record_id.root)
                result = await session.execute(stmt)
                sa_user = result.scalar_one_or_none()

                if sa_user is None:
                    return RepositoryResponse[User | None](
                        response=None,
                        is_success=RepositoryResultStatusEnum.SUCCESS,
                        status=RepositoryResponseStatusEnum.READ,
                    )

                domain_user = SAUserTranslator.to_domain(sa_user)

                return RepositoryResponse[User | None](
                    response=domain_user,
                    is_success=RepositoryResultStatusEnum.SUCCESS,
                    status=RepositoryResponseStatusEnum.READ,
                )

        except Exception as e:
            return RepositoryResponse[User | None](
                response=None,
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
                reason=RepositoryFailedResponseEnum.UNKNOWN,
                message=f"Failed to get user: {str(e)}",
            )

    @logfire.instrument(span_name="SAUserRepository.get_by_user_id_and_messenger()")
    async def get_by_user_id_and_messenger(
        self, user_id: UserID, messenger_record_id: UserMessengerRecordID
    ) -> RepositoryResponse[User | None]:
        try:
            async with self.session_factory() as session:
                stmt = select(SAUser).where(
                    SAUser.user_id == user_id.root,
                    SAUser.messenger_record_id == messenger_record_id.root,
                )
                result = await session.execute(stmt)
                sa_user = result.scalar_one_or_none()

                if sa_user is None:
                    return RepositoryResponse[User | None](
                        response=None,
                        is_success=RepositoryResultStatusEnum.SUCCESS,
                        status=RepositoryResponseStatusEnum.READ,
                    )

                domain_user = SAUserTranslator.to_domain(sa_user)

                return RepositoryResponse[User | None](
                    response=domain_user,
                    is_success=RepositoryResultStatusEnum.SUCCESS,
                    status=RepositoryResponseStatusEnum.READ,
                )

        except Exception as e:
            return RepositoryResponse[User | None](
                response=None,
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
                reason=RepositoryFailedResponseEnum.UNKNOWN,
                message=f"Failed to get user by user_id and messenger: {str(e)}",
            )

    @logfire.instrument(span_name="SAUserRepository.get_or_create()")
    async def get_or_create(self, user: User) -> RepositoryResponse[User | None]:
        # まず既存のユーザーを検索
        get_response = await self.get_by_user_id_and_messenger(
            user.id, user.messenger_record_id
        )

        if get_response.is_success == RepositoryResultStatusEnum.ERROR:
            return get_response

        if get_response.response is not None:
            return get_response

        # 存在しない場合は新規作成
        return await self.create(user)
