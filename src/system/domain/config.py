from abc import abstractmethod
from enum import StrEnum

from src.config.interface import ConfigIf


class EnvironmentEnum(StrEnum):
    TEST = "TEST"
    PRODUCTION = "PRODUCTION"
    DEVELOPMENT = "DEVELOPMENT"


class DomainConfigIf(ConfigIf):
    # noinspection PyPep8Naming
    @property
    @abstractmethod
    def ENVIRONMENT(self) -> EnvironmentEnum:
        pass
