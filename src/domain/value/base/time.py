from datetime import datetime

from pydantic import Field, RootModel

from src.util.datetime import utcnow


class DatetimeBase(RootModel[datetime]):
    pass


class CreatedAtBase(DatetimeBase):
    root: datetime = Field(default_factory=utcnow)


class UpdatedAtBase(DatetimeBase):
    root: datetime = Field(default_factory=utcnow)
