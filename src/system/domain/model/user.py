from src.system.domain.model.base import DomainModelBase
from src.system.domain.value.user import (
    UserRecordID,
    UserCreatedAt,
    UserUpdatedAt,
    UserID,
    UserMessengerRecordID,
)


class User(DomainModelBase):
    record_id: UserRecordID
    created_at: UserCreatedAt
    updated_at: UserUpdatedAt
    messenger_record_id: UserMessengerRecordID
    id: UserID
