from typing import TypeVar
from ulid import ULID

from pydantic import RootModel

from src.common.interface import Interface

IDType = TypeVar("IDType")


class IDBase[IDType](Interface):
    pass


class ULIDBase(IDBase[ULID], RootModel[ULID]):
    pass
