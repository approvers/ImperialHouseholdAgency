from src.system.domain.model.base import DomainModelBase
from src.system.domain.value.messenger import (
    MessengerCreatedAt,
    MessengerName,
    MessengerRecordID,
    MessengerUpdatedAt,
)


class Messenger(DomainModelBase):
    record_id: MessengerRecordID
    created_at: MessengerCreatedAt
    updated_at: MessengerUpdatedAt
    name: MessengerName
