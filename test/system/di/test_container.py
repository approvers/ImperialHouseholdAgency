from injector import Injector

from src.system.domain.config import DomainConfigIf
from src.system.di.container import DIContainer
from src.system.infrastructure.repository.sqlalchemy.config import SQLAlchemyConfigIf
from src.system.infrastructure.sentry.config import SentryConfigIf
from src.system.ui.discord.config import DiscordConfigIf

SHOULD_BE_ABLE_TO_GET: list[type] = [
    DomainConfigIf,
    SQLAlchemyConfigIf,
    DiscordConfigIf,
    SentryConfigIf,
]


def test_can_get_concreate_class(
    container: Injector = DIContainer,
) -> None:
    for abstract_class in SHOULD_BE_ABLE_TO_GET:
        # noinspection PyTypeChecker
        concreate_class = container.get(abstract_class)  # type: ignore[var-annotated]

        assert concreate_class is not None
        assert isinstance(concreate_class, abstract_class)
