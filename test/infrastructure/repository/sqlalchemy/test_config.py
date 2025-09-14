import pytest

from src.infrastructure.repository.sqlalchemy.config import SQLAlchemyConfigIF


def test_sqlalchemy_config_if_is_abstract() -> None:
    with pytest.raises(TypeError):
        SQLAlchemyConfigIF()  # type: ignore[abstract]
