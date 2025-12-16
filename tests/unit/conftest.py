"""Shared fixtures for unit tests."""

import pytest


@pytest.fixture
def sample_json_content() -> str:
    """Return sample JSON content for testing."""
    return '{"name": "test", "value": 42}'


@pytest.fixture
def sample_csv_content() -> str:
    """Return sample CSV content for testing."""
    return "name,value\ntest,42"
