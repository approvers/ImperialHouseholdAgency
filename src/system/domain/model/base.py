from pydantic import BaseModel

from src.system.common.interface import Interface


class DomainModelBase(BaseModel, Interface):
    pass
