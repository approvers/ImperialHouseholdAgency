from src.system.domain.model.user import User as DomainUser
from src.system.infrastructure.repository.sqlalchemy.model.user import User as SAUser
from src.system.infrastructure.repository.sqlalchemy.translator.base import (
    BaseSADomainTranslator,
)


class SAUserTranslator(BaseSADomainTranslator[DomainUser, SAUser]):
    @staticmethod
    def to_domain(db_record: SAUser) -> DomainUser:
        from src.system.domain.value.user import (
            UserRecordID,
            UserCreatedAt,
            UserUpdatedAt,
            UserMessengerRecordID,
            UserID,
        )

        result = DomainUser(
            record_id=UserRecordID(db_record.record_id),
            created_at=UserCreatedAt(db_record.created_at),
            updated_at=UserUpdatedAt(db_record.updated_at),
            messenger_record_id=UserMessengerRecordID(db_record.messenger_record_id),
            id=UserID(db_record.user_id),
        )

        return result

    @staticmethod
    def to_db_record(domain_model: DomainUser) -> SAUser:
        result = SAUser(
            record_id=domain_model.record_id.root,
            created_at=domain_model.created_at.root,
            updated_at=domain_model.updated_at.root,
            messenger_record_id=domain_model.messenger_record_id.root,
            user_id=domain_model.id.root,
        )

        return result
