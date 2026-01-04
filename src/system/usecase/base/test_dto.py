from src.system.usecase.base.dto import (
    UsecaseBaseDTO,
    UsecaseRequest,
    UsecaseResponse,
)


def test_usecase_base_dto_is_instantiable() -> None:
    dto = UsecaseBaseDTO()
    assert dto is not None


def test_usecase_request_is_instantiable() -> None:
    request = UsecaseRequest()
    assert request is not None


def test_usecase_request_inherits_from_usecase_base_dto() -> None:
    assert issubclass(UsecaseRequest, UsecaseBaseDTO)


def test_usecase_response_is_instantiable() -> None:
    response = UsecaseResponse()
    assert response is not None


def test_usecase_response_inherits_from_usecase_base_dto() -> None:
    assert issubclass(UsecaseResponse, UsecaseBaseDTO)
