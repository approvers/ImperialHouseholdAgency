from config import get_config_for_current_env
from src.common.di.builder import ModuleBase, BindEntry

from injector import SingletonScope

from src.system.ui.discord.config import DiscordConfigIf


class PydanticDiscordConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=DiscordConfigIf,
            to=get_config_for_current_env(),
            scope=SingletonScope,
        ),
    )
