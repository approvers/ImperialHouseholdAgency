from abc import abstractmethod
from typing import TypeVar

from src.common.interface import Interface

DBModelT = TypeVar("DBModelT")
DomainT = TypeVar("DomainT")


class BaseSQLAlchemyDomainTranslator[DomainT, DBModelT](Interface):
    @staticmethod
    @abstractmethod
    def to_domain(db_record: DBModelT) -> DomainT:
        pass

    @staticmethod
    @abstractmethod
    def to_db_record(domain_model: DomainT) -> DBModelT:
        pass
