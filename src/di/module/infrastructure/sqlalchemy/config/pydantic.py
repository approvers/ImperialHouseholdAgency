from injector import SingletonScope

from config import get_config_for_current_env
from src.di.builder import ModuleBase, BindEntry
from src.infrastructure.repository.sqlalchemy.config import SQLAlchemyConfigIF


class PydanticSQLAlchemyConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=SQLAlchemyConfigIF,
            to=get_config_for_current_env(),
            scope=SingletonScope,
        ),
    )
