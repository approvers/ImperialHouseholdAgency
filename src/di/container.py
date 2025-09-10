from typing import Final, Iterable

from injector import Injector, Module

from src.di.module.domain.config.pydantic import PydanticDomainConfigModule

# NOTE:
#   Change here to change dependencies to load!
__MODULES: Final[Iterable[Module]] = (PydanticDomainConfigModule(),)

DIContainer: Final[Injector] = Injector(
    modules=__MODULES,
    auto_bind=False,
)
