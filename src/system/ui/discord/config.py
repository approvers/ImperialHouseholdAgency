from abc import abstractmethod

from src.common.interface import ConfigIF


# noinspection PyPep8Naming
class DiscordConfigIF(ConfigIF):
    @property
    @abstractmethod
    def DISCORD_TOKEN(self) -> str:
        pass
