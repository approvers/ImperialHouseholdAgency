from abc import abstractmethod
from typing import TypeVar

from src.system.common.interface import Interface
from src.system.domain.model.base import DomainModelBase
from src.system.infrastructure.repository.sqlalchemy.model.base import Base

DomainT = TypeVar("DomainT", bound=DomainModelBase)
SAModelT = TypeVar("SAModelT", bound=Base)


class BaseSADomainTranslator[DomainT, SAModelT](Interface):
    @staticmethod
    @abstractmethod
    def to_domain(db_record: SAModelT) -> DomainT:
        pass

    @staticmethod
    @abstractmethod
    def to_db_record(domain_model: DomainT) -> SAModelT:
        pass
