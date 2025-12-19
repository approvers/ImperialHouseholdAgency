from src.system.domain.model.nickname import (
    NicknameChangelog as DomainNicknameChangelog,
)
from src.system.infrastructure.repository.sqlalchemy.model.nickname import (
    NicknameChangelog as SANicknameChangelog,
)
from src.system.infrastructure.repository.sqlalchemy.translator.base import (
    BaseSADomainTranslator,
)


class SANicknameChangelogTranslator(
    BaseSADomainTranslator[DomainNicknameChangelog, SANicknameChangelog]
):
    @staticmethod
    def to_domain(db_record: SANicknameChangelog) -> DomainNicknameChangelog:
        result = DomainNicknameChangelog(
            record_id=db_record.record_id,
            created_at=db_record.created_at,
            user_record_id=db_record.user_record_id,
            before=db_record.before,
            after=db_record.after,
        )

        return result

    @staticmethod
    def to_db_record(domain_model: DomainNicknameChangelog) -> SANicknameChangelog:
        result = SANicknameChangelog(
            record_id=domain_model.record_id.root,
            created_at=domain_model.created_at.root,
            user_record_id=domain_model.user_record_id.root,
            before=domain_model.before.root,
            after=domain_model.after.root,
        )

        return result
