from unittest.mock import MagicMock, patch

from injector import Binder, singleton

from src.system.di.module.infrastructure.repository.sqlalchemy.module import (
    SARepositoryModule,
)
from src.system.domain.interface.repository.messenger import MessengerRepository
from src.system.domain.interface.repository.nickname import NicknameChangelogRepository
from src.system.domain.interface.repository.user import UserRepository
from src.system.infrastructure.repository.sqlalchemy.config import SQLAlchemyConfigIf
from src.system.infrastructure.repository.sqlalchemy.crud.messenger import (
    SAMessengerRepository,
)
from src.system.infrastructure.repository.sqlalchemy.crud.nickname import (
    SANicknameChangelogRepository,
)
from src.system.infrastructure.repository.sqlalchemy.crud.user import (
    SAUserRepository,
)


class MockSQLAlchemyConfig(SQLAlchemyConfigIf):
    @property
    def DATABASE_URL(self) -> str:
        return "postgresql+asyncpg://test:test@localhost/test"


class TestSARepositoryModule:
    def test_configure_binds_all_repositories(self) -> None:
        module = SARepositoryModule()
        binder = MagicMock(spec=Binder)

        module.configure(binder)

        assert binder.bind.call_count == 3

        # MessengerRepositoryのバインディングを検証
        messenger_call = binder.bind.call_args_list[0]
        assert messenger_call.kwargs["interface"] is MessengerRepository
        assert messenger_call.kwargs["to"] is SAMessengerRepository
        assert messenger_call.kwargs["scope"] is singleton

        # UserRepositoryのバインディングを検証
        user_call = binder.bind.call_args_list[1]
        assert user_call.kwargs["interface"] is UserRepository
        assert user_call.kwargs["to"] is SAUserRepository
        assert user_call.kwargs["scope"] is singleton

        # NicknameChangelogRepositoryのバインディングを検証
        nickname_call = binder.bind.call_args_list[2]
        assert nickname_call.kwargs["interface"] is NicknameChangelogRepository
        assert nickname_call.kwargs["to"] is SANicknameChangelogRepository
        assert nickname_call.kwargs["scope"] is singleton

    @patch(
        "src.system.di.module.infrastructure.repository.sqlalchemy.module.create_async_engine"
    )
    def test_provide_sa_async_session_factory_creates_engine(
        self, mock_create_engine: MagicMock
    ) -> None:
        # SARepositoryModule._engineをリセット
        SARepositoryModule._engine = None

        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        module = SARepositoryModule()
        config = MockSQLAlchemyConfig()

        session_factory = module.provide_sa_async_session_factory(config)

        assert session_factory is not None
        mock_create_engine.assert_called_once_with(config.DATABASE_URL)
        assert SARepositoryModule._engine is mock_engine

    @patch(
        "src.system.di.module.infrastructure.repository.sqlalchemy.module.create_async_engine"
    )
    def test_provide_sa_async_session_factory_reuses_engine(
        self, mock_create_engine: MagicMock
    ) -> None:
        # SARepositoryModule._engineをリセット
        SARepositoryModule._engine = None

        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        module = SARepositoryModule()
        config = MockSQLAlchemyConfig()

        # 1回目の呼び出し
        _ = module.provide_sa_async_session_factory(config)
        engine1 = SARepositoryModule._engine

        # 2回目の呼び出し（同じエンジンを使い回す）
        _ = module.provide_sa_async_session_factory(config)
        engine2 = SARepositoryModule._engine

        # エンジンは1回だけ作成される
        mock_create_engine.assert_called_once()
        assert engine1 is engine2
