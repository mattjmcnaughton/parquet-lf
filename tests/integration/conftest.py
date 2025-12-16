"""Shared fixtures for integration tests."""

from pathlib import Path

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
def sample_ndjson_file(sample_ndjson_content: str, tmp_path: Path) -> Path:
    """Create a temporary NDJSON file with sample content."""
    ndjson_file = tmp_path / "sample.ndjson"
    ndjson_file.write_text(sample_ndjson_content)
    return ndjson_file


@pytest.fixture
def sample_csv_file(sample_csv_content: str, tmp_path: Path) -> Path:
    """Create a temporary CSV file with sample content."""
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(sample_csv_content)
    return csv_file


@pytest.fixture
def sample_parquet_file(tmp_path: Path) -> Path:
    """Create a temporary Parquet file with sample data."""
    parquet_file = tmp_path / "sample.parquet"
    df = pl.DataFrame({"name": ["test", "hello"], "value": [42, 100]})
    df.write_parquet(parquet_file)
    return parquet_file


@pytest.fixture
def sample_dataframe() -> pl.DataFrame:
    """Return a sample Polars DataFrame for testing."""
    return pl.DataFrame({"name": ["test", "hello"], "value": [42, 100]})
