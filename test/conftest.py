import pytest
from ulid import ULID

from src.util.id import generate_ulid


@pytest.fixture
def sample_ulid() -> ULID:
    """Generate a sample ULID for testing."""
    return generate_ulid()


@pytest.fixture
def sample_ulid_str(sample_ulid: ULID) -> str:
    """Generate a sample ULID string for testing."""
    return str(sample_ulid)


@pytest.fixture
def dialect() -> object:
    """Provide a simple dialect object for testing."""

    class SimpleDialect:
        pass

    return SimpleDialect()
