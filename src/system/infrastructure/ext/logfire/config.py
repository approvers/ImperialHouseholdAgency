from abc import abstractmethod

from src.common.config.interface import ConfigIf


class LogfireConfigIf(ConfigIf):
    @property
    @abstractmethod
    def LOGFIRE_WRITE_TOKEN(self) -> str | None:
        pass
