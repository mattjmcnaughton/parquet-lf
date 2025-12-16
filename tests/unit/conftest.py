"""Shared fixtures for unit tests."""

import polars as pl
import pytest


@pytest.fixture
def sample_ndjson_content() -> str:
    """Return sample NDJSON content for testing (one JSON object per line)."""
    return '{"name": "test", "value": 42}\n{"name": "hello", "value": 100}'


@pytest.fixture
def sample_csv_content() -> str:
    """Return sample CSV content for testing."""
    return "name,value\ntest,42\nhello,100"


@pytest.fixture
def sample_dataframe() -> pl.DataFrame:
    """Return a sample Polars DataFrame for testing."""
    return pl.DataFrame({"name": ["test", "hello"], "value": [42, 100]})
