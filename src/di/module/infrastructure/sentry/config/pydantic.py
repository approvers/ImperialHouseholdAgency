from injector import SingletonScope

from config import get_config_for_current_env
from src.di.builder import ModuleBase, BindEntry
from src.infrastructure.sentry.config import SentryConfigIF


class PydanticSentryConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=SentryConfigIF,
            to=get_config_for_current_env(),
            scope=SingletonScope,
        ),
    )
