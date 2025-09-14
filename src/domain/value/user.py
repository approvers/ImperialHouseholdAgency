from pydantic import RootModel

from src.domain.value.messenger import MessengerID


class UserMessengerID(MessengerID):
    pass


class UserID(RootModel[str]):
    pass
