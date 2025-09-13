from config import get_config_for_current_env
from src.di.builder import ModuleBase, BindEntry

from injector import SingletonScope

from src.ui.discord.config import DiscordConfigIF


class PydanticDiscordConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=DiscordConfigIF,
            to=get_config_for_current_env(),
            scope=SingletonScope,
        ),
    )
