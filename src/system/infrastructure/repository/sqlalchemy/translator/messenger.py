from src.system.domain.model.messenger import Messenger as DomainMessenger
from src.system.infrastructure.repository.sqlalchemy.model.messenger import (
    Messenger as SAMessenger,
)
from src.system.infrastructure.repository.sqlalchemy.translator.base import (
    BaseSADomainTranslator,
)


class SAMessengerTranslator(BaseSADomainTranslator[DomainMessenger, SAMessenger]):
    @staticmethod
    def to_domain(db_record: SAMessenger) -> DomainMessenger:
        from src.system.domain.value.messenger import (
            MessengerRecordID,
            MessengerCreatedAt,
            MessengerUpdatedAt,
            MessengerName,
        )

        result = DomainMessenger(
            record_id=MessengerRecordID(db_record.record_id),
            created_at=MessengerCreatedAt(db_record.created_at),
            updated_at=MessengerUpdatedAt(db_record.updated_at),
            name=MessengerName(db_record.name),
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
