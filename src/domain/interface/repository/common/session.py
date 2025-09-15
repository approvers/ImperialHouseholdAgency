from abc import abstractmethod
from typing import AsyncGenerator, Generator

from src.common.interface import Interface


class SessionIF(Interface):
    pass


class AsyncSessionIF(SessionIF):
    pass


class SessionProviderIF[SessionT: SessionIF](Interface, Generator):
    @abstractmethod
    def __enter__(self) -> SessionIF:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class AsyncSessionProviderIF[SessionT: SessionIF](Interface, AsyncGenerator):
    @abstractmethod
    async def __aenter__(self) -> SessionIF:
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
