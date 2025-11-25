import logfire

from src.system.di.container import DIContainer
from src.system.domain.config import DomainConfigIf
from src.system.infrastructure.logfire.config import LogfireConfigIf


def init_logfire(
    *,
    domain_config: DomainConfigIf | None = None,
    logfire_config: LogfireConfigIf | None = None,
) -> None:
    actual_domain_config = domain_config or DIContainer.get(DomainConfigIf)  # type: ignore [type-abstract]
    actual_logfire_config = logfire_config or DIContainer.get(LogfireConfigIf)  # type: ignore [type-abstract]

    if actual_logfire_config.LOGFIRE_WRITE_TOKEN is None:
        return

    logfire.configure(
        token=actual_logfire_config.LOGFIRE_WRITE_TOKEN,
        environment=actual_domain_config.ENVIRONMENT,
    )
