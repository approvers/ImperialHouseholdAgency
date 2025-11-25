from src.system.domain.model.base import DomainModelBase
from src.system.domain.value.messenger import (
    MessengerRecordID,
    MessengerCreatedAt,
    MessengerUpdatedAt,
    MessengerName,
)


class Messenger(DomainModelBase):
    record_id: MessengerRecordID
    created_at: MessengerCreatedAt
    updated_at: MessengerUpdatedAt
    name: MessengerName
