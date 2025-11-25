import sentry_sdk

from src.system.di.container import DIContainer
from src.system.infrastructure.sentry.config import SentryConfigIf


def init_sentry(config: SentryConfigIf | None = None) -> None:
    actual_config = config or DIContainer.get(SentryConfigIf)  # type: ignore [type-abstract]

    if not actual_config.SENTRY_DSN and not actual_config.SENTRY_DSN:
        sentry_sdk.init(
            dsn=str(actual_config.SENTRY_DSN),
            send_default_pii=True,
        )
