from abc import abstractmethod

from src.common.interface import ConfigIF


class SQLAlchemyConfigIF(ConfigIF):
    @property
    @abstractmethod
    def uri(self) -> str:
        pass
