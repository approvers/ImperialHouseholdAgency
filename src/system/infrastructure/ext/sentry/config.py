from abc import abstractmethod

from src.common.config.interface import ConfigIf


class SentryConfigIf(ConfigIf):
    @property
    @abstractmethod
    def SENTRY_DSN(self) -> str:
        pass

    @property
    @abstractmethod
    def SENTRY_ENV(self) -> str:
        pass
