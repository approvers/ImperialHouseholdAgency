from typing import Final, Iterable

from injector import Injector, Module

from src.system.di.module.domain.config.pydantic import PydanticDomainConfigModule
from src.system.di.module.infrastructure.logfire.config.pydantic import (
    PydanticLogfireConfigModule,
)
from src.system.di.module.infrastructure.repository.sqlalchemy.config.pydantic import (
    PydanticSQLAlchemyConfigModule,
)
from src.system.di.module.infrastructure.repository.sqlalchemy.module import (
    SARepositoryModule,
)
from src.system.di.module.infrastructure.sentry.config.pydantic import (
    PydanticSentryConfigModule,
)
from src.system.di.module.ui.discord.config.pydantic import PydanticDiscordConfigModule

# NOTE:
#   Change here to change dependencies to load!
__MODULES: Final[Iterable[Module]] = (
    PydanticDomainConfigModule(),
    PydanticLogfireConfigModule(),
    PydanticSQLAlchemyConfigModule(),
    SARepositoryModule(),
    PydanticSentryConfigModule(),
    PydanticDiscordConfigModule(),
)

DIContainer: Final[Injector] = Injector(
    modules=__MODULES,
    auto_bind=False,
)
