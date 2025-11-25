import sentry_sdk

from src.system.di.container import DIContainer
from src.system.infrastructure.sentry.config import SentryConfigIF


def init_sentry() -> None:
    config = DIContainer.get(SentryConfigIF)  # type: ignore [type-abstract]

    sentry_sdk.init(
        dsn=str(config.SENTRY_DSN),
        send_default_pii=True,
    )
