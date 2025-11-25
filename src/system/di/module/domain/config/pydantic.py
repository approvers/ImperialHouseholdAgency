from injector import SingletonScope

from config import get_config_for_current_env
from src.common.di.builder import ModuleBase, BindEntry
from src.system.domain.config import DomainConfigIf


class PydanticDomainConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=DomainConfigIf,
            to=get_config_for_current_env(),
            scope=SingletonScope,
        ),
    )
