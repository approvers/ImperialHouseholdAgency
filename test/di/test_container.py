from injector import Injector

from src.domain.config import DomainConfigIF
from src.di.container import DIContainer
from src.infrastructure.repository.sqlalchemy.config import SQLAlchemyConfigIF
from src.infrastructure.sentry.config import SentryConfigIF
from src.ui.discord.config import DiscordConfigIF

SHOULD_BE_ABLE_TO_GET: list[type] = [
    DomainConfigIF,
    SQLAlchemyConfigIF,
    DiscordConfigIF,
    SentryConfigIF,
]


def test_can_get_concreate_class(
    container: Injector = DIContainer,
) -> None:
    for abstract_class in SHOULD_BE_ABLE_TO_GET:
        # noinspection PyTypeChecker
        concreate_class = container.get(abstract_class)  # type: ignore[var-annotated]

        assert concreate_class is not None
        assert isinstance(concreate_class, abstract_class)
