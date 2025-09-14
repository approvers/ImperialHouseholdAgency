import pytest

from src.domain.config import DomainConfigIF, EnvironmentEnum


def test_environment_enum_test_value() -> None:
    assert EnvironmentEnum.TEST == "TEST"


def test_environment_enum_production_value() -> None:
    assert EnvironmentEnum.PRODUCTION == "PRODUCTION"


def test_environment_enum_development_value() -> None:
    assert EnvironmentEnum.DEVELOPMENT == "DEVELOPMENT"


def test_environment_enum_all_values() -> None:
    assert len(EnvironmentEnum) == 3
    assert set(EnvironmentEnum) == {
        EnvironmentEnum.TEST,
        EnvironmentEnum.PRODUCTION,
        EnvironmentEnum.DEVELOPMENT,
    }


def test_domain_config_if_is_abstract() -> None:
    with pytest.raises(TypeError):
        DomainConfigIF()  # type: ignore[abstract]
