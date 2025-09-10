from injector import Injector

from src.domain.config import DomainConfigIF
from src.di.container import DIContainer


SHOULD_BE_ABLE_TO_GET: list[type] = [DomainConfigIF]


def test_can_get_concreate_class(
    container: Injector = DIContainer,
) -> None:
    for abstract_class in SHOULD_BE_ABLE_TO_GET:
        # noinspection PyTypeChecker
        concreate_class = container.get(abstract_class)  # type: ignore[var-annotated]

        assert concreate_class is not None
        assert isinstance(concreate_class, abstract_class)
