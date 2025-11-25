from abc import abstractmethod

from src.common.config.interface import ConfigIf


class SQLAlchemyConfigIf(ConfigIf):
    # noinspection PyPep8Naming
    @property
    @abstractmethod
    def DATABASE_URL(self) -> str:
        pass
