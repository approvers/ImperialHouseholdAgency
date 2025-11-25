from abc import abstractmethod

from src.common.interface import ConfigIF


class SentryConfigIF(ConfigIF):
    @property
    @abstractmethod
    def SENTRY_DSN(self) -> str:
        pass

    @property
    @abstractmethod
    def SENTRY_ENV(self) -> str:
        pass
