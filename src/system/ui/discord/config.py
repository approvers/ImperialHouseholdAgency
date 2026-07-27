from abc import abstractmethod

from src.common.config.interface import ConfigIf


# noinspection PyPep8Naming
class DiscordConfigIf(ConfigIf):
    @property
    @abstractmethod
    def DISCORD_TOKEN(self) -> str:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def ERROR_NOTIFICATION_CHANNEL_ID(self) -> int | None:
        """Channel ID for error notifications. If None, uses guild system channel."""
        pass  # pragma: no cover
