from typing import AsyncGenerator

from src.common.interface import Interface


class SessionIF(Interface):
    pass


class SessionProvider(Interface, AsyncGenerator):
    def __init__(self):
        pass

    async def __aenter__(self) -> SessionIF:
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
