from abc import abstractmethod

from src.common.interface import Interface
from src.system.domain.model.event.base import EventBase
from src.system.handler.context import HandlerContext


class EventHandlerIf[EventT: EventBase](Interface):
    """Base interface for event handlers."""

    @abstractmethod
    async def handle(self, context: HandlerContext, event: EventT) -> None:
        """Handle an event.

        Args:
            context: Handler context with tracing information.
            event: The event to handle.
        """
        pass  # pragma: no cover
