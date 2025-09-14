from src.domain.model.base import DomainModelBase
from src.domain.value.nickname import (
    NicknameChangelogCreatedAt,
    NicknameChangelogBefore,
    NicknameChangelogAfter,
)


class NicknameChangelog(DomainModelBase):
    created_at: NicknameChangelogCreatedAt
    before: NicknameChangelogBefore
    after: NicknameChangelogAfter
