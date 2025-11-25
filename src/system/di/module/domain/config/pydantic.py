from injector import SingletonScope

from config import get_config_for_current_env
from src.system.di.builder import ModuleBase, BindEntry
from src.system.domain.config import DomainConfigIF


class PydanticDomainConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=DomainConfigIF,
            to=get_config_for_current_env(),
            scope=SingletonScope,
        ),
    )
