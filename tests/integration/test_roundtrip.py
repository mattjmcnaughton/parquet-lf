"""Integration tests for round-trip conversions."""

from pathlib import Path

import polars as pl
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from parquet_lf.converters.csv import csv_to_parquet, parquet_to_csv
from parquet_lf.converters.ndjson import ndjson_to_parquet, parquet_to_ndjson


class TestCSVRoundtrip:
    """Tests for CSV <-> Parquet round-trip conversions."""

    def test_csv_to_parquet_basic(self, sample_csv_file: Path, tmp_path: Path) -> None:
        """CSV file converts to valid Parquet."""
        output_path = tmp_path / "output.parquet"
        csv_to_parquet(sample_csv_file, output_path)

        assert output_path.exists()
        df = pl.read_parquet(output_path)
        assert df.shape == (2, 2)
        assert df.columns == ["name", "value"]

    def test_parquet_to_csv_basic(self, sample_parquet_file: Path, tmp_path: Path) -> None:
        """Parquet file converts to valid CSV."""
        output_path = tmp_path / "output.csv"
        parquet_to_csv(sample_parquet_file, output_path)

        assert output_path.exists()
        df = pl.read_csv(output_path)
        assert df.shape == (2, 2)
        assert df.columns == ["name", "value"]

    def test_csv_roundtrip_preserves_data(self, sample_csv_file: Path, tmp_path: Path) -> None:
        """CSV -> Parquet -> CSV preserves data."""
        parquet_path = tmp_path / "intermediate.parquet"
        csv_output_path = tmp_path / "output.csv"

        csv_to_parquet(sample_csv_file, parquet_path)
        parquet_to_csv(parquet_path, csv_output_path)

        original_df = pl.read_csv(sample_csv_file)
        roundtrip_df = pl.read_csv(csv_output_path)

        assert original_df.equals(roundtrip_df)

    def test_csv_file_not_found(self, tmp_path: Path) -> None:
        """FileNotFoundError raised for missing CSV file."""
        nonexistent = tmp_path / "nonexistent.csv"
        output_path = tmp_path / "output.parquet"

        with pytest.raises(FileNotFoundError):
            csv_to_parquet(nonexistent, output_path)

    def test_parquet_file_not_found_for_csv(self, tmp_path: Path) -> None:
        """FileNotFoundError raised for missing Parquet file."""
        nonexistent = tmp_path / "nonexistent.parquet"
        output_path = tmp_path / "output.csv"

        with pytest.raises(FileNotFoundError):
            parquet_to_csv(nonexistent, output_path)


class TestNDJSONRoundtrip:
    """Tests for NDJSON <-> Parquet round-trip conversions."""

    def test_ndjson_to_parquet_basic(self, sample_ndjson_file: Path, tmp_path: Path) -> None:
        """NDJSON file converts to valid Parquet."""
        output_path = tmp_path / "output.parquet"
        ndjson_to_parquet(sample_ndjson_file, output_path)

        assert output_path.exists()
        df = pl.read_parquet(output_path)
        assert df.shape == (2, 2)
        assert set(df.columns) == {"name", "value"}

    def test_parquet_to_ndjson_basic(self, sample_parquet_file: Path, tmp_path: Path) -> None:
        """Parquet file converts to valid NDJSON."""
        output_path = tmp_path / "output.ndjson"
        parquet_to_ndjson(sample_parquet_file, output_path)

        assert output_path.exists()
        df = pl.read_ndjson(output_path)
        assert df.shape == (2, 2)
        assert set(df.columns) == {"name", "value"}

    def test_ndjson_roundtrip_preserves_data(self, sample_ndjson_file: Path, tmp_path: Path) -> None:
        """NDJSON -> Parquet -> NDJSON preserves data."""
        parquet_path = tmp_path / "intermediate.parquet"
        ndjson_output_path = tmp_path / "output.ndjson"

        ndjson_to_parquet(sample_ndjson_file, parquet_path)
        parquet_to_ndjson(parquet_path, ndjson_output_path)

        original_df = pl.read_ndjson(sample_ndjson_file)
        roundtrip_df = pl.read_ndjson(ndjson_output_path)

        assert original_df.equals(roundtrip_df)

    def test_ndjson_file_not_found(self, tmp_path: Path) -> None:
        """FileNotFoundError raised for missing NDJSON file."""
        nonexistent = tmp_path / "nonexistent.ndjson"
        output_path = tmp_path / "output.parquet"

        with pytest.raises(FileNotFoundError):
            ndjson_to_parquet(nonexistent, output_path)

    def test_parquet_file_not_found_for_ndjson(self, tmp_path: Path) -> None:
        """FileNotFoundError raised for missing Parquet file."""
        nonexistent = tmp_path / "nonexistent.parquet"
        output_path = tmp_path / "output.ndjson"

        with pytest.raises(FileNotFoundError):
            parquet_to_ndjson(nonexistent, output_path)


class TestCrossFormatConversion:
    """Tests for cross-format conversions."""

    def test_csv_to_parquet_to_ndjson(self, sample_csv_file: Path, tmp_path: Path) -> None:
        """CSV -> Parquet -> NDJSON preserves data."""
        parquet_path = tmp_path / "intermediate.parquet"
        ndjson_path = tmp_path / "output.ndjson"

        csv_to_parquet(sample_csv_file, parquet_path)
        parquet_to_ndjson(parquet_path, ndjson_path)

        original_df = pl.read_csv(sample_csv_file)
        final_df = pl.read_ndjson(ndjson_path)

        assert original_df.equals(final_df)

    def test_ndjson_to_parquet_to_csv(self, sample_ndjson_file: Path, tmp_path: Path) -> None:
        """NDJSON -> Parquet -> CSV preserves data."""
        parquet_path = tmp_path / "intermediate.parquet"
        csv_path = tmp_path / "output.csv"

        ndjson_to_parquet(sample_ndjson_file, parquet_path)
        parquet_to_csv(parquet_path, csv_path)

        original_df = pl.read_ndjson(sample_ndjson_file)
        final_df = pl.read_csv(csv_path)

        assert original_df.equals(final_df)


class TestHypothesisRoundtrip:
    """Property-based tests using Hypothesis."""

    @given(
        data=st.lists(
            st.fixed_dictionaries(
                {
                    "name": st.text(
                        alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_"),
                        min_size=1,
                        max_size=50,
                    ).filter(
                        # Filter out strings that look like numbers to avoid CSV type inference issues
                        lambda x: not x.lstrip("-").isdigit()
                    ),
                    "value": st.integers(min_value=-1000000, max_value=1000000),
                }
            ),
            min_size=1,
            max_size=100,
        )
    )
    @settings(max_examples=20)
    def test_csv_roundtrip_hypothesis(self, data: list[dict], tmp_path_factory) -> None:
        """Property-based test: CSV round-trip preserves data for various inputs."""
        tmp_path = tmp_path_factory.mktemp("csv_hypothesis")
        df = pl.DataFrame(data)

        csv_path = tmp_path / "input.csv"
        parquet_path = tmp_path / "intermediate.parquet"
        output_csv_path = tmp_path / "output.csv"

        df.write_csv(csv_path)
        csv_to_parquet(csv_path, parquet_path)
        parquet_to_csv(parquet_path, output_csv_path)

        roundtrip_df = pl.read_csv(output_csv_path)
        assert df.equals(roundtrip_df)

    @given(
        data=st.lists(
            st.fixed_dictionaries(
                {
                    "name": st.text(min_size=1, max_size=50).filter(lambda x: "\n" not in x and "\r" not in x),
                    "value": st.integers(min_value=-1000000, max_value=1000000),
                }
            ),
            min_size=1,
            max_size=100,
        )
    )
    @settings(max_examples=20)
    def test_ndjson_roundtrip_hypothesis(self, data: list[dict], tmp_path_factory) -> None:
        """Property-based test: NDJSON round-trip preserves data for various inputs."""
        tmp_path = tmp_path_factory.mktemp("ndjson_hypothesis")
        df = pl.DataFrame(data)

        ndjson_path = tmp_path / "input.ndjson"
        parquet_path = tmp_path / "intermediate.parquet"
        output_ndjson_path = tmp_path / "output.ndjson"

        df.write_ndjson(ndjson_path)
        ndjson_to_parquet(ndjson_path, parquet_path)
        parquet_to_ndjson(parquet_path, output_ndjson_path)

        roundtrip_df = pl.read_ndjson(output_ndjson_path)
        assert df.equals(roundtrip_df)
