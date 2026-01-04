from injector import Module, Binder, singleton, provider
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
    create_async_engine,
)

from src.system.domain.interface.repository.messenger import MessengerRepository
from src.system.infrastructure.repository.sqlalchemy.config import SQLAlchemyConfigIf
from src.system.infrastructure.repository.sqlalchemy.crud.messenger import (
    SAMessengerRepository,
)


class SARepositoryModule(Module):
    _engine: AsyncEngine | None = None

    @provider
    @singleton
    def provide_sa_async_session_factory(
        self, config: SQLAlchemyConfigIf
    ) -> async_sessionmaker[AsyncSession]:
        if SARepositoryModule._engine is None:
            SARepositoryModule._engine = create_async_engine(config.DATABASE_URL)

        session_maker = async_sessionmaker(
            SARepositoryModule._engine, expire_on_commit=False
        )
        return session_maker

    def configure(self, binder: Binder) -> None:
        binder.bind(
            interface=MessengerRepository,  # type: ignore[type-abstract]
            to=SAMessengerRepository,
            scope=singleton,
        )
