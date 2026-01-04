import pytest

from src.system.usecase.base.interface import UsecaseIf


def test_usecase_if_is_abstract() -> None:
    with pytest.raises(TypeError):
        UsecaseIf()  # type: ignore[abstract]
