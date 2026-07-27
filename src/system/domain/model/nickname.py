from src.system.domain.model.base import DomainModelBase
from src.system.domain.value.nickname import (
    NicknameChangelogAfter,
    NicknameChangelogBefore,
    NicknameChangelogCreatedAt,
    NicknameChangelogRecordID,
    NicknameChangelogUserRecordID,
)


class NicknameChangelog(DomainModelBase):
    record_id: NicknameChangelogRecordID
    created_at: NicknameChangelogCreatedAt
    user_record_id: NicknameChangelogUserRecordID
    before: NicknameChangelogBefore
    after: NicknameChangelogAfter
