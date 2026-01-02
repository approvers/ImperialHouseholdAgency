from pydantic import Field

import logfire
import sentry_sdk

from src.system.domain.model.base import DomainModelBase
from src.system.domain.value.base.identifier import ULIDBase


class HandlerID(ULIDBase):
    """Unique identifier for handler invocation, used for tracing."""

    pass


class HandlerContext(DomainModelBase):
    """Context for handler invocation with tracing capabilities."""

    handler_id: HandlerID = Field(default_factory=HandlerID)

    def setup_tracing(self) -> None:
        """Set up tracing with Sentry and Logfire."""
        handler_id_str = str(self.handler_id.root)

        # Sentry タグを設定
        sentry_sdk.set_tag("handler_id", handler_id_str)

        # Logfire スパンを設定
        logfire.info("Handler invoked", handler_id=handler_id_str)
