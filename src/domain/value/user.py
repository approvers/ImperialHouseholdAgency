from pydantic import RootModel

from src.domain.value.base.identifier import ULIDBase
from src.domain.value.base.time import CreatedAtBase, UpdatedAtBase
from src.domain.value.messenger import MessengerRecordID


class UserRecordID(ULIDBase):
    pass


class UserCreatedAt(CreatedAtBase):
    pass


class UserUpdatedAt(UpdatedAtBase):
    pass


class UserMessengerRecordID(MessengerRecordID):
    pass


class UserID(RootModel[str]):
    pass
