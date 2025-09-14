from pydantic import BaseModel

from src.domain.value.nickname import (
    NicknameChangelogCreatedAt,
    NicknameChangelogBefore,
    NicknameChangelogAfter,
)


class NicknameChangelog(BaseModel):
    created_at: NicknameChangelogCreatedAt
    before: NicknameChangelogBefore
    after: NicknameChangelogAfter
