from injector import SingletonScope

from config import ImperialHouseholdAgencyConfig
from src.di.builder import ModuleBase, BindEntry
from src.domain.config import DomainConfigIF
from src.ui.discord.config import DiscordConfigIF


class PydanticDomainConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=DomainConfigIF,
            to=ImperialHouseholdAgencyConfig,
            scope=SingletonScope,
        ),
        BindEntry(
            interface=DiscordConfigIF,
            to=ImperialHouseholdAgencyConfig,
            scope=SingletonScope,
        ),
    )
