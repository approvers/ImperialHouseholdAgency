from injector import SingletonScope

from config import get_config_for_current_env
from src.common.di.builder import ModuleBase, BindEntry
from src.system.infrastructure.repository.sqlalchemy.config import SQLAlchemyConfigIf


class PydanticSQLAlchemyConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=SQLAlchemyConfigIf,
            to=get_config_for_current_env(),
            scope=SingletonScope,
        ),
    )
