from pydantic import RootModel

from src.system.domain.value.base.identifier import ULIDBase
from src.system.domain.value.base.time import CreatedAtBase
from src.system.domain.value.user import UserRecordID


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
