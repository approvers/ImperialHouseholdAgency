from injector import SingletonScope

from config import get_config_for_current_env
from src.common.di.builder import BindEntry, ModuleBase
from src.system.infrastructure.logfire.config import LogfireConfigIf


class PydanticLogfireConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=LogfireConfigIf,
            to=get_config_for_current_env(),
            scope=SingletonScope,
        ),
    )
