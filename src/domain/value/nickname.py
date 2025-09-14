from pydantic import RootModel

from src.domain.value.base.identifier import ULIDBase
from src.domain.value.base.time import CreatedAtBase
from src.domain.value.user import UserRecordID


class NicknameChangelogRecordID(ULIDBase):
    pass


class NicknameChangelogCreatedAt(CreatedAtBase):
    pass


class NicknameChangelogUserRecordID(UserRecordID):
    pass


class Nickname(RootModel[str]):
    pass


class NicknameChangelogBefore(Nickname):
    pass


class NicknameChangelogAfter(Nickname):
    pass
