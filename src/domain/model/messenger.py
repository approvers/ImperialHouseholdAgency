from pydantic import BaseModel

from src.domain.value.messenger import (
    MessengerRecordID,
    MessengerCreatedAt,
    MessengerUpdatedAt,
    MessengerName,
)


class Messenger(BaseModel):
    record_id: MessengerRecordID
    created_at: MessengerCreatedAt
    updated_at: MessengerUpdatedAt
    name: MessengerName
