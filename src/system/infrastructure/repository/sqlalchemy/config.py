from abc import abstractmethod

from src.system.common.interface import ConfigIF


class SQLAlchemyConfigIF(ConfigIF):
    # noinspection PyPep8Naming
    @property
    @abstractmethod
    def DATABASE_URL(self) -> str:
        pass
