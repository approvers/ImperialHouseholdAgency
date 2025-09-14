from typing import Any, List

import pytest
from pydantic import ValidationError

from src.domain.interface.repository.common.response import (
    RepositoryFailedResponseEnum,
    RepositoryResponse,
    RepositoryResponseStatusEnum,
    RepositoryResultStatusEnum,
)
from src.domain.model.base import DomainModelBase


class MockDomainModel(DomainModelBase):
    name: str
    value: int


class TestRepositoryResultStatusEnum:
    def test_success_value(self) -> None:
        assert RepositoryResultStatusEnum.SUCCESS == "SUCCESS"

    def test_error_value(self) -> None:
        assert RepositoryResultStatusEnum.ERROR == "ERROR"

    def test_all_values(self) -> None:
        assert len(RepositoryResultStatusEnum) == 2
        assert set(RepositoryResultStatusEnum) == {
            RepositoryResultStatusEnum.SUCCESS,
            RepositoryResultStatusEnum.ERROR,
        }


class TestRepositoryResponseStatusEnum:
    def test_created_value(self) -> None:
        assert RepositoryResponseStatusEnum.CREATED == "CREATED"

    def test_read_value(self) -> None:
        assert RepositoryResponseStatusEnum.READ == "READ"

    def test_updated_value(self) -> None:
        assert RepositoryResponseStatusEnum.UPDATED == "UPDATED"

    def test_deleted_value(self) -> None:
        assert RepositoryResponseStatusEnum.DELETED == "DELETED"

    def test_failed_value(self) -> None:
        assert RepositoryResponseStatusEnum.FAILED == "FAILED"

    def test_all_values(self) -> None:
        assert len(RepositoryResponseStatusEnum) == 5
        assert set(RepositoryResponseStatusEnum) == {
            RepositoryResponseStatusEnum.CREATED,
            RepositoryResponseStatusEnum.READ,
            RepositoryResponseStatusEnum.UPDATED,
            RepositoryResponseStatusEnum.DELETED,
            RepositoryResponseStatusEnum.FAILED,
        }


class TestRepositoryFailedResponseEnum:
    def test_unknown_value(self) -> None:
        assert RepositoryFailedResponseEnum.UNKNOWN == "UNKNOWN"

    def test_all_values(self) -> None:
        assert len(RepositoryFailedResponseEnum) == 1
        assert set(RepositoryFailedResponseEnum) == {
            RepositoryFailedResponseEnum.UNKNOWN,
        }


class TestRepositoryResponse:
    def test_successful_creation_with_response(self) -> None:
        model = MockDomainModel(name="test", value=42)
        response = RepositoryResponse[MockDomainModel](
            response=model,
            is_success=RepositoryResultStatusEnum.SUCCESS,
            status=RepositoryResponseStatusEnum.CREATED,
        )

        assert response.response == model
        assert response.is_success == RepositoryResultStatusEnum.SUCCESS
        assert response.status == RepositoryResponseStatusEnum.CREATED
        assert response.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert response.message is None

    def test_successful_read_with_list_response(self) -> None:
        models = [
            MockDomainModel(name="test1", value=1),
            MockDomainModel(name="test2", value=2),
        ]
        response = RepositoryResponse[List[MockDomainModel]](
            response=models,
            is_success=RepositoryResultStatusEnum.SUCCESS,
            status=RepositoryResponseStatusEnum.READ,
        )

        assert response.response == models
        assert response.is_success == RepositoryResultStatusEnum.SUCCESS
        assert response.status == RepositoryResponseStatusEnum.READ
        assert response.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert response.message is None

    def test_successful_update_with_none_response(self) -> None:
        response = RepositoryResponse[None](
            response=None,
            is_success=RepositoryResultStatusEnum.SUCCESS,
            status=RepositoryResponseStatusEnum.UPDATED,
        )

        assert response.response is None
        assert response.is_success == RepositoryResultStatusEnum.SUCCESS
        assert response.status == RepositoryResponseStatusEnum.UPDATED
        assert response.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert response.message is None

    def test_successful_deletion(self) -> None:
        response = RepositoryResponse[None](
            response=None,
            is_success=RepositoryResultStatusEnum.SUCCESS,
            status=RepositoryResponseStatusEnum.DELETED,
        )

        assert response.response is None
        assert response.is_success == RepositoryResultStatusEnum.SUCCESS
        assert response.status == RepositoryResponseStatusEnum.DELETED
        assert response.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert response.message is None

    def test_failed_response_with_message(self) -> None:
        response = RepositoryResponse[None](
            response=None,
            is_success=RepositoryResultStatusEnum.ERROR,
            status=RepositoryResponseStatusEnum.FAILED,
            reason=RepositoryFailedResponseEnum.UNKNOWN,
            message="Something went wrong",
        )

        assert response.response is None
        assert response.is_success == RepositoryResultStatusEnum.ERROR
        assert response.status == RepositoryResponseStatusEnum.FAILED
        assert response.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert response.message == "Something went wrong"

    def test_failed_response_with_custom_reason(self) -> None:
        response = RepositoryResponse[None](
            response=None,
            is_success=RepositoryResultStatusEnum.ERROR,
            status=RepositoryResponseStatusEnum.FAILED,
            reason=RepositoryFailedResponseEnum.UNKNOWN,
            message="Database connection failed",
        )

        assert response.response is None
        assert response.is_success == RepositoryResultStatusEnum.ERROR
        assert response.status == RepositoryResponseStatusEnum.FAILED
        assert response.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert response.message == "Database connection failed"

    def test_success_with_explicit_none_message(self) -> None:
        response = RepositoryResponse[None](
            response=None,
            is_success=RepositoryResultStatusEnum.SUCCESS,
            status=RepositoryResponseStatusEnum.READ,
            message=None,
        )

        assert response.response is None
        assert response.is_success == RepositoryResultStatusEnum.SUCCESS
        assert response.status == RepositoryResponseStatusEnum.READ
        assert response.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert response.message is None

    def test_success_with_message_allowed(self) -> None:
        response = RepositoryResponse[None](
            response=None,
            is_success=RepositoryResultStatusEnum.SUCCESS,
            status=RepositoryResponseStatusEnum.READ,
            message="Successfully retrieved data",
        )

        assert response.response is None
        assert response.is_success == RepositoryResultStatusEnum.SUCCESS
        assert response.status == RepositoryResponseStatusEnum.READ
        assert response.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert response.message == "Successfully retrieved data"

    def test_validator_error_when_failed_without_message(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            RepositoryResponse[None](
                response=None,
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
            )

        error = exc_info.value
        assert len(error.errors()) == 1
        assert error.errors()[0]["type"] == "value_error"
        assert (
            "'self.reason' is required when 'self.is_success' is set to 'ERROR'"
            in str(error)
        )

    def test_validator_error_when_failed_with_empty_message(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            RepositoryResponse[None](
                response=None,
                is_success=RepositoryResultStatusEnum.ERROR,
                status=RepositoryResponseStatusEnum.FAILED,
                message="",
            )

        error = exc_info.value
        assert len(error.errors()) == 1
        assert error.errors()[0]["type"] == "value_error"
        assert (
            "'self.reason' is required when 'self.is_success' is set to 'ERROR'"
            in str(error)
        )

    def test_validator_passes_when_success_without_message(self) -> None:
        # This should not raise an exception
        response = RepositoryResponse[None](
            response=None,
            is_success=RepositoryResultStatusEnum.SUCCESS,
            status=RepositoryResponseStatusEnum.READ,
        )

        assert response.message is None

    def test_validator_passes_when_failed_with_message(self) -> None:
        # This should not raise an exception
        response = RepositoryResponse[None](
            response=None,
            is_success=RepositoryResultStatusEnum.ERROR,
            status=RepositoryResponseStatusEnum.FAILED,
            message="Error occurred",
        )

        assert response.message == "Error occurred"

    def test_generic_type_with_any(self) -> None:
        arbitrary_data = {"key": "value", "number": 42}
        response = RepositoryResponse[Any](
            response=arbitrary_data,
            is_success=RepositoryResultStatusEnum.SUCCESS,
            status=RepositoryResponseStatusEnum.READ,
        )

        assert response.response == arbitrary_data
        assert response.is_success == RepositoryResultStatusEnum.SUCCESS
        assert response.status == RepositoryResponseStatusEnum.READ

    def test_all_status_combinations(self) -> None:
        model = MockDomainModel(name="test", value=1)

        # Test all successful status combinations
        for status in [
            RepositoryResponseStatusEnum.CREATED,
            RepositoryResponseStatusEnum.READ,
            RepositoryResponseStatusEnum.UPDATED,
            RepositoryResponseStatusEnum.DELETED,
        ]:
            response = RepositoryResponse[MockDomainModel](
                response=model,
                is_success=RepositoryResultStatusEnum.SUCCESS,
                status=status,
            )
            assert response.status == status
            assert response.is_success == RepositoryResultStatusEnum.SUCCESS

        # Test failed status
        failed_response = RepositoryResponse[None](
            response=None,
            is_success=RepositoryResultStatusEnum.ERROR,
            status=RepositoryResponseStatusEnum.FAILED,
            message="Test error",
        )
        assert failed_response.status == RepositoryResponseStatusEnum.FAILED
        assert failed_response.is_success == RepositoryResultStatusEnum.ERROR

    def test_default_values(self) -> None:
        response = RepositoryResponse[None](
            response=None,
            is_success=RepositoryResultStatusEnum.SUCCESS,
            status=RepositoryResponseStatusEnum.READ,
        )

        # Test default values
        assert response.reason == RepositoryFailedResponseEnum.UNKNOWN
        assert response.message is None

    def test_explicit_reason_override(self) -> None:
        response = RepositoryResponse[None](
            response=None,
            is_success=RepositoryResultStatusEnum.ERROR,
            status=RepositoryResponseStatusEnum.FAILED,
            reason=RepositoryFailedResponseEnum.UNKNOWN,
            message="Test message",
        )

        assert response.reason == RepositoryFailedResponseEnum.UNKNOWN
