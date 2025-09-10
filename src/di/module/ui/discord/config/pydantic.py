from config import ImperialHouseholdAgencyConfig
from src.di.builder import ModuleBase, BindEntry

from injector import SingletonScope

from src.ui.discord.config import DiscordConfigIF


class PydanticDiscordConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=DiscordConfigIF,
            to=ImperialHouseholdAgencyConfig,
            scope=SingletonScope,
        ),
    )
