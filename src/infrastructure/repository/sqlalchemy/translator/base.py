from abc import abstractmethod
from typing import TypeVar

from src.common.interface import Interface
from src.domain.model.base import DomainModelBase
from src.infrastructure.repository.sqlalchemy.model.base import Base

DomainT = TypeVar("DomainT", bound=DomainModelBase)
DBModelT = TypeVar("DBModelT", bound=Base)


class BaseSQLAlchemyDomainTranslator[DomainT, DBModelT](Interface):
    @staticmethod
    @abstractmethod
    def to_domain(db_record: DBModelT) -> DomainT:
        pass

    @staticmethod
    @abstractmethod
    def to_db_record(domain_model: DomainT) -> DBModelT:
        pass
