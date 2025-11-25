from abc import abstractmethod
from enum import StrEnum

from src.system.common.interface import ConfigIF


class EnvironmentEnum(StrEnum):
    TEST = "TEST"
    PRODUCTION = "PRODUCTION"
    DEVELOPMENT = "DEVELOPMENT"


class DomainConfigIF(ConfigIF):
    # noinspection PyPep8Naming
    @property
    @abstractmethod
    def ENVIRONMENT(self) -> EnvironmentEnum:
        pass
