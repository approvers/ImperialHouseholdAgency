from pydantic import BaseModel

from src.domain.value.user import (
    UserRecordID,
    UserCreatedAt,
    UserUpdatedAt,
    UserID,
    UserMessengerRecordID,
)


class User(BaseModel):
    record_id: UserRecordID
    created_at: UserCreatedAt
    updated_at: UserUpdatedAt
    messenger_record_id: UserMessengerRecordID
    id: UserID
