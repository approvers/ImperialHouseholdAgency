from src.domain.model.messenger import Messenger as DomainMessenger
from src.infrastructure.repository.sqlalchemy.model.messenger import (
    Messenger as SAMessenger,
)
from src.infrastructure.repository.sqlalchemy.translator.base import (
    BaseSADomainTranslator,
)


class SAMessengerTranslator(
    BaseSADomainTranslator[DomainMessenger, SAMessenger]
):
    @staticmethod
    def to_domain(db_record: SAMessenger) -> DomainMessenger:
        # noinspection PyTypeChecker,PydanticTypeChecker
        result = DomainMessenger(
            record_id=db_record.record_id,
            created_at=db_record.created_at,
            updated_at=db_record.updated_at,
            name=db_record.name,
        )

        return result

    @staticmethod
    def to_db_record(domain_model: DomainMessenger) -> SAMessenger:
        result = SAMessenger()

        result.record_id = domain_model.record_id.root
        result.created_at = domain_model.created_at.root
        result.updated_at = domain_model.updated_at.root
        result.name = domain_model.name.root

        return result
