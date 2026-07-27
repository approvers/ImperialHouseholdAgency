from typing import TypeVar

from pydantic import Field, RootModel
from ulid import ULID

from src.common.interface import Interface
from src.system.util.id import generate_ulid

IDType = TypeVar("IDType")


class IDBase[IDType](Interface):
    pass


class ULIDBase(IDBase[ULID], RootModel[ULID]):
    root: ULID = Field(default_factory=generate_ulid)
