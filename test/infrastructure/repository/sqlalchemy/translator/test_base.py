import pytest

from src.infrastructure.repository.sqlalchemy.translator.base import (
    BaseSADomainTranslator,
)


def test_base_sa_domain_translator_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseSADomainTranslator()  # type: ignore[abstract]
