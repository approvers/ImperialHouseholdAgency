from pydantic import BaseModel

from src.common.interface import Interface


class DomainModelBase(BaseModel, Interface):
    pass
