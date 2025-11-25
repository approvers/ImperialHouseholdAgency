from pydantic import RootModel

from src.system.domain.value.base.identifier import ULIDBase
from src.system.domain.value.base.time import CreatedAtBase, UpdatedAtBase


class MessengerRecordID(ULIDBase):
    pass


class MessengerCreatedAt(CreatedAtBase):
    pass


class MessengerUpdatedAt(UpdatedAtBase):
    pass


class MessengerName(RootModel[str]):
    pass
