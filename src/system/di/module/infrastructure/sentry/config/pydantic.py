from injector import SingletonScope

from config import get_config_for_current_env
from src.system.di.builder import ModuleBase, BindEntry
from src.system.infrastructure.sentry.config import SentryConfigIf


class PydanticSentryConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=SentryConfigIf,
            to=get_config_for_current_env(),
            scope=SingletonScope,
        ),
    )
