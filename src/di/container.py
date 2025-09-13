from typing import Final, Iterable

from injector import Injector, Module

from src.di.module.domain.config.pydantic import PydanticDomainConfigModule
from src.di.module.infrastructure.sqlalchemy.config.pydantic import (
    PydanticSQLAlchemyConfigModule,
)
from src.di.module.ui.discord.config.pydantic import PydanticDiscordConfigModule

# NOTE:
#   Change here to change dependencies to load!
__MODULES: Final[Iterable[Module]] = (
    PydanticDomainConfigModule(),
    PydanticSQLAlchemyConfigModule(),
    PydanticDiscordConfigModule(),
)

DIContainer: Final[Injector] = Injector(
    modules=__MODULES,
    auto_bind=False,
)
