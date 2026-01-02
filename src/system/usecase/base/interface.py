from abc import abstractmethod

from src.common.interface import Interface
from src.system.usecase.base.dto import UsecaseRequest, UsecaseResponse


class UsecaseIf[RequestT: UsecaseRequest, ResponseT: UsecaseResponse](Interface):
    """Base interface for use cases."""

    @abstractmethod
    async def execute(self, request: RequestT) -> ResponseT:
        """Execute the use case.

        Args:
            request: The use case request.

        Returns:
            The use case response.
        """
        pass  # pragma: no cover
