from pydantic import RootModel

from src.domain.value.base.identifier import ULIDBase
from src.domain.value.base.time import CreatedAtBase, UpdatedAtBase


class MessengerID(ULIDBase):
    pass


class MessengerCreatedAt(CreatedAtBase):
    pass


class MessengerUpdatedAt(UpdatedAtBase):
    pass


class MessengerName(RootModel[str]):
    pass
