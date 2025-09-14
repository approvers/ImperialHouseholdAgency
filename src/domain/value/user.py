from pydantic import RootModel

from src.domain.value.base.identifier import ULIDBase
from src.domain.value.messenger import MessengerID


class UserRecordID(ULIDBase):
    pass


class UserMessengerID(MessengerID):
    pass


class UserID(RootModel[str]):
    pass
