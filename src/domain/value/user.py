from pydantic import RootModel

from src.domain.value.base.identifier import ULIDBase
from src.domain.value.base.time import CreatedAtBase
from src.domain.value.messenger import MessengerRecordID


class UserRecordID(ULIDBase):
    pass


class UserCreatedAt(CreatedAtBase):
    pass


class UserMessengerRecordID(MessengerRecordID):
    pass


class UserID(RootModel[str]):
    pass
