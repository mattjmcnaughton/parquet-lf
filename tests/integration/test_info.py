"""Integration tests for the info module.

These tests cover functions that interact with the filesystem.
"""

from pathlib import Path

import polars as pl
import pytest

from parquet_lf.info import FileFormat, get_file_info, get_file_info_with_preview


class TestGetFileInfo:
    """Tests for the get_file_info function with real files."""

    def test_parquet_file_info(self, sample_parquet_file: Path) -> None:
        """Test get_file_info with a Parquet file."""
        info = get_file_info(sample_parquet_file)

        assert info.path == sample_parquet_file
        assert info.format == FileFormat.PARQUET
        assert info.size_bytes > 0
        assert info.row_count == 2
        assert info.column_count == 2
        assert "name" in info.schema
        assert "value" in info.schema

    def test_csv_file_info(self, sample_csv_file: Path) -> None:
        """Test get_file_info with a CSV file."""
        info = get_file_info(sample_csv_file)

        assert info.path == sample_csv_file
        assert info.format == FileFormat.CSV
        assert info.size_bytes > 0
        assert info.row_count == 2
        assert info.column_count == 2
        assert "name" in info.schema
        assert "value" in info.schema

    def test_ndjson_file_info(self, sample_ndjson_file: Path) -> None:
        """Test get_file_info with an NDJSON file."""
        info = get_file_info(sample_ndjson_file)

        assert info.path == sample_ndjson_file
        assert info.format == FileFormat.NDJSON
        assert info.size_bytes > 0
        assert info.row_count == 2
        assert info.column_count == 2
        assert "name" in info.schema
        assert "value" in info.schema

    def test_nonexistent_file_raises_error(self, tmp_path: Path) -> None:
        """Test get_file_info raises FileNotFoundError for missing file."""
        nonexistent = tmp_path / "nonexistent.parquet"

        with pytest.raises(FileNotFoundError, match="Input file not found"):
            get_file_info(nonexistent)

    def test_unsupported_extension_raises_error(self, tmp_path: Path) -> None:
        """Test get_file_info raises ValueError for unsupported extension."""
        unsupported = tmp_path / "test.xyz"
        unsupported.write_text("some content")

        with pytest.raises(ValueError, match="Unsupported file extension"):
            get_file_info(unsupported)

    def test_empty_parquet_file(self, tmp_path: Path) -> None:
        """Test get_file_info with empty Parquet file (0 rows)."""
        empty_file = tmp_path / "empty.parquet"
        df = pl.DataFrame({"col": []}).cast({"col": pl.String})
        df.write_parquet(empty_file)

        info = get_file_info(empty_file)

        assert info.row_count == 0
        assert info.column_count == 1

    def test_jsonl_extension_detected_as_ndjson(self, tmp_path: Path) -> None:
        """Test .jsonl extension is detected as NDJSON format."""
        jsonl_file = tmp_path / "test.jsonl"
        jsonl_file.write_text('{"a": 1}\n{"a": 2}')

        info = get_file_info(jsonl_file)

        assert info.format == FileFormat.NDJSON


class TestGetFileInfoWithPreview:
    """Tests for the get_file_info_with_preview function."""

    def test_returns_info_and_preview(self, sample_parquet_file: Path) -> None:
        """Test function returns both file info and preview."""
        info, preview = get_file_info_with_preview(sample_parquet_file, 1)

        assert info.path == sample_parquet_file
        assert info.format == FileFormat.PARQUET
        assert info.row_count == 2
        assert len(preview) == 1

    def test_preview_matches_head_count(self, sample_parquet_file: Path) -> None:
        """Test preview has correct number of rows."""
        info, preview = get_file_info_with_preview(sample_parquet_file, 2)

        assert len(preview) == 2

    def test_works_with_csv(self, sample_csv_file: Path) -> None:
        """Test function works with CSV files."""
        info, preview = get_file_info_with_preview(sample_csv_file, 1)

        assert info.format == FileFormat.CSV
        assert len(preview) == 1

    def test_works_with_ndjson(self, sample_ndjson_file: Path) -> None:
        """Test function works with NDJSON files."""
        info, preview = get_file_info_with_preview(sample_ndjson_file, 1)

        assert info.format == FileFormat.NDJSON
        assert len(preview) == 1

    def test_nonexistent_file_raises_error(self, tmp_path: Path) -> None:
        """Test raises FileNotFoundError for missing file."""
        nonexistent = tmp_path / "nonexistent.parquet"

        with pytest.raises(FileNotFoundError, match="Input file not found"):
            get_file_info_with_preview(nonexistent, 5)

    def test_info_matches_standalone_function(self, sample_parquet_file: Path) -> None:
        """Test info from combined function matches standalone get_file_info."""
        info_standalone = get_file_info(sample_parquet_file)
        info_combined, _ = get_file_info_with_preview(sample_parquet_file, 1)

        assert info_standalone.row_count == info_combined.row_count
        assert info_standalone.column_count == info_combined.column_count
        assert info_standalone.schema == info_combined.schema
