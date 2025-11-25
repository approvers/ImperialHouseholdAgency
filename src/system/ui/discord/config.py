from abc import abstractmethod

from src.config.interface import ConfigIf


# noinspection PyPep8Naming
class DiscordConfigIf(ConfigIf):
    @property
    @abstractmethod
    def DISCORD_TOKEN(self) -> str:
        pass
