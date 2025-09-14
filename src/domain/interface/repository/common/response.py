from enum import StrEnum
from typing import Self, Iterable

from pydantic import BaseModel, Field, model_validator

from src.domain.model.base import DomainModelBase


class RepositoryResultStatusEnum(StrEnum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class RepositoryResponseStatusEnum(StrEnum):
    CREATED = "CREATED"
    READ = "READ"
    UPDATED = "UPDATED"
    DELETED = "DELETED"
    FAILED = "FAILED"


class RepositoryFailedResponseEnum(StrEnum):
    UNKNOWN = "UNKNOWN"


class RepositoryResponse[ResponseT: DomainModelBase | Iterable[DomainModelBase] | None](
    BaseModel
):
    response: ResponseT
    is_success: RepositoryResultStatusEnum
    status: RepositoryResponseStatusEnum
    reason: RepositoryFailedResponseEnum = Field(
        default=RepositoryFailedResponseEnum.UNKNOWN
    )
    message: str | None = Field(default=None)

    @model_validator(mode="after")
    def must_have_message_when_failed(self) -> Self:
        if self.is_success == RepositoryResultStatusEnum.ERROR and not self.message:
            raise ValueError(
                "'self.message' is required when 'self.is_success' is set to 'ERROR'"
            )

        return self
