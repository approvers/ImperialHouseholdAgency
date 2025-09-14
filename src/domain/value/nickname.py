from pydantic import RootModel

from src.domain.value.base.identifier import ULIDBase
from src.domain.value.base.time import CreatedAtBase


class NicknameChangelogID(ULIDBase):
    pass


class NicknameChangelogCreatedAt(CreatedAtBase):
    pass


class Nickname(RootModel[str]):
    pass


class NicknameChangelogBefore(Nickname):
    pass


class NicknameChangelogAfter(Nickname):
    pass
