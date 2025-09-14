from datetime import datetime

from pydantic import RootModel


class DatetimeBase(RootModel[datetime]):
    pass


class CreatedAtBase(DatetimeBase):
    pass


class UpdatedAtBase(DatetimeBase):
    pass
