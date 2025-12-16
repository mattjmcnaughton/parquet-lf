"""Unit tests for the info module.

These tests cover pure logic functions without filesystem operations.
"""

from pathlib import Path

import pytest

from parquet_lf.info import (
    BYTES_PER_GB,
    BYTES_PER_KB,
    BYTES_PER_MB,
    FileFormat,
    FileInfo,
    detect_format,
    format_file_info,
    format_size,
)


class TestDetectFormat:
    """Tests for the detect_format function."""

    def test_parquet_extension(self) -> None:
        """Test .parquet extension returns PARQUET format."""
        assert detect_format(Path("test.parquet")) == FileFormat.PARQUET

    def test_csv_extension(self) -> None:
        """Test .csv extension returns CSV format."""
        assert detect_format(Path("test.csv")) == FileFormat.CSV

    def test_ndjson_extension(self) -> None:
        """Test .ndjson extension returns NDJSON format."""
        assert detect_format(Path("test.ndjson")) == FileFormat.NDJSON

    def test_jsonl_extension_returns_ndjson(self) -> None:
        """Test .jsonl extension returns NDJSON format (alias)."""
        assert detect_format(Path("test.jsonl")) == FileFormat.NDJSON

    def test_case_insensitive_parquet(self) -> None:
        """Test uppercase .PARQUET extension."""
        assert detect_format(Path("test.PARQUET")) == FileFormat.PARQUET

    def test_case_insensitive_csv(self) -> None:
        """Test mixed case .Csv extension."""
        assert detect_format(Path("test.Csv")) == FileFormat.CSV

    def test_case_insensitive_ndjson(self) -> None:
        """Test uppercase .NDJSON extension."""
        assert detect_format(Path("test.NDJSON")) == FileFormat.NDJSON

    def test_case_insensitive_jsonl(self) -> None:
        """Test uppercase .JSONL extension."""
        assert detect_format(Path("test.JSONL")) == FileFormat.NDJSON

    def test_unknown_extension_raises_value_error(self) -> None:
        """Test unknown extension raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported file extension: .xyz"):
            detect_format(Path("test.xyz"))

    def test_no_extension_raises_value_error(self) -> None:
        """Test file without extension raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported file extension:"):
            detect_format(Path("testfile"))

    def test_path_with_directory(self) -> None:
        """Test path with directory components."""
        assert detect_format(Path("/some/dir/test.parquet")) == FileFormat.PARQUET


class TestFormatSize:
    """Tests for the format_size function."""

    def test_bytes(self) -> None:
        """Test size in bytes."""
        assert format_size(500) == "500 B"

    def test_zero_bytes(self) -> None:
        """Test zero bytes."""
        assert format_size(0) == "0 B"

    def test_one_byte(self) -> None:
        """Test one byte."""
        assert format_size(1) == "1 B"

    def test_just_under_kb(self) -> None:
        """Test size just under 1 KB."""
        assert format_size(BYTES_PER_KB - 1) == "1023 B"

    def test_exactly_one_kb(self) -> None:
        """Test exactly 1 KB."""
        assert format_size(BYTES_PER_KB) == "1.0 KB"

    def test_kilobytes(self) -> None:
        """Test size in kilobytes."""
        assert format_size(int(1.5 * BYTES_PER_KB)) == "1.5 KB"

    def test_just_under_mb(self) -> None:
        """Test size just under 1 MB."""
        assert format_size(BYTES_PER_MB - 1) == "1024.0 KB"

    def test_exactly_one_mb(self) -> None:
        """Test exactly 1 MB."""
        assert format_size(BYTES_PER_MB) == "1.0 MB"

    def test_megabytes(self) -> None:
        """Test size in megabytes."""
        assert format_size(int(2.5 * BYTES_PER_MB)) == "2.5 MB"

    def test_just_under_gb(self) -> None:
        """Test size just under 1 GB."""
        assert format_size(BYTES_PER_GB - 1) == "1024.0 MB"

    def test_exactly_one_gb(self) -> None:
        """Test exactly 1 GB."""
        assert format_size(BYTES_PER_GB) == "1.0 GB"

    def test_gigabytes(self) -> None:
        """Test size in gigabytes."""
        assert format_size(int(3.5 * BYTES_PER_GB)) == "3.5 GB"


class TestFormatFileInfo:
    """Tests for the format_file_info function."""

    def test_basic_output_structure(self) -> None:
        """Test basic output structure without preview."""
        info = FileInfo(
            path=Path("test.parquet"),
            format=FileFormat.PARQUET,
            size_bytes=1024,
            row_count=100,
            column_count=3,
            schema={"name": "String", "age": "Int64", "score": "Float64"},
        )
        output = format_file_info(info)

        assert "File: test.parquet" in output
        assert "Format: Parquet" in output
        assert "Size: 1.0 KB" in output
        assert "Rows: 100" in output
        assert "Columns: 3" in output
        assert "Schema:" in output
        assert "  name: String" in output
        assert "  age: Int64" in output
        assert "  score: Float64" in output

    def test_csv_format_display(self) -> None:
        """Test CSV format is displayed correctly."""
        info = FileInfo(
            path=Path("test.csv"),
            format=FileFormat.CSV,
            size_bytes=500,
            row_count=10,
            column_count=2,
            schema={"a": "Int64", "b": "String"},
        )
        output = format_file_info(info)

        assert "Format: Csv" in output

    def test_ndjson_format_display(self) -> None:
        """Test NDJSON format is displayed correctly."""
        info = FileInfo(
            path=Path("test.ndjson"),
            format=FileFormat.NDJSON,
            size_bytes=500,
            row_count=10,
            column_count=2,
            schema={"a": "Int64", "b": "String"},
        )
        output = format_file_info(info)

        assert "Format: Ndjson" in output

    def test_no_preview_section_when_none(self) -> None:
        """Test no preview section when preview is None."""
        info = FileInfo(
            path=Path("test.parquet"),
            format=FileFormat.PARQUET,
            size_bytes=1024,
            row_count=100,
            column_count=1,
            schema={"col": "String"},
        )
        output = format_file_info(info, preview=None)

        assert "Preview" not in output

    def test_empty_schema(self) -> None:
        """Test formatting with empty schema."""
        info = FileInfo(
            path=Path("test.parquet"),
            format=FileFormat.PARQUET,
            size_bytes=0,
            row_count=0,
            column_count=0,
            schema={},
        )
        output = format_file_info(info)

        assert "Rows: 0" in output
        assert "Columns: 0" in output
        assert "Schema:" in output


class TestFileFormat:
    """Tests for the FileFormat enum."""

    def test_parquet_value(self) -> None:
        """Test PARQUET enum value."""
        assert FileFormat.PARQUET.value == "parquet"

    def test_csv_value(self) -> None:
        """Test CSV enum value."""
        assert FileFormat.CSV.value == "csv"

    def test_ndjson_value(self) -> None:
        """Test NDJSON enum value."""
        assert FileFormat.NDJSON.value == "ndjson"
