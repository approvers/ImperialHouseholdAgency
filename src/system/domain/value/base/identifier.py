from typing import TypeVar
from ulid import ULID

from pydantic import RootModel, Field

from src.common.interface import Interface
from src.system.util.id import generate_ulid

IDType = TypeVar("IDType")


class IDBase[IDType](Interface):
    pass


class ULIDBase(IDBase[ULID], RootModel[ULID]):
    root: ULID = Field(default_factory=generate_ulid)
