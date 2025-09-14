from src.domain.model.base import DomainModelBase
from src.domain.value.nickname import (
    NicknameChangelogRecordID,
    NicknameChangelogCreatedAt,
    NicknameChangelogUserRecordID,
    NicknameChangelogBefore,
    NicknameChangelogAfter,
)


class NicknameChangelog(DomainModelBase):
    record_id: NicknameChangelogRecordID
    created_at: NicknameChangelogCreatedAt
    user_record_id: NicknameChangelogUserRecordID
    before: NicknameChangelogBefore
    after: NicknameChangelogAfter
