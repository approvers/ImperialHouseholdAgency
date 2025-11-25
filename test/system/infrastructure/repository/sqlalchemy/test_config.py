import pytest

from src.system.infrastructure.repository.sqlalchemy.config import SQLAlchemyConfigIf


def test_sqlalchemy_config_if_is_abstract() -> None:
    with pytest.raises(TypeError):
        SQLAlchemyConfigIf()  # type: ignore[abstract]
