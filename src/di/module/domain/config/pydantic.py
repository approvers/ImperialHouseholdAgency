from injector import SingletonScope

from config import ImperialHouseholdAgencyConfig
from src.di.builder import ModuleBase, BindEntry
from src.domain.config import DomainConfigIF


class PydanticDomainConfigModule(ModuleBase):
    _BINDINGS = (
        BindEntry(
            interface=DomainConfigIF,
            to=ImperialHouseholdAgencyConfig,
            scope=SingletonScope,
        ),
    )
