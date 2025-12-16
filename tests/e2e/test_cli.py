"""End-to-end tests for CLI commands."""

from pathlib import Path

import polars as pl


class TestToParquetCSV:
    """E2E tests for to-parquet csv command."""

    def test_csv_to_parquet_with_output_file(self, run_cli, tmp_path: Path) -> None:
        """CLI converts CSV to Parquet with -o flag."""
        csv_file = tmp_path / "input.csv"
        csv_file.write_text("name,value\nalice,10\nbob,20")
        output_file = tmp_path / "output.parquet"

        result = run_cli(["to-parquet", "csv", str(csv_file), "-o", str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()
        df = pl.read_parquet(output_file)
        assert df.shape == (2, 2)

    def test_csv_to_parquet_stdout_via_redirect(self, run_cli, tmp_path: Path) -> None:
        """CLI outputs Parquet to stdout when using dash as output."""
        csv_file = tmp_path / "input.csv"
        csv_file.write_text("name,value\ntest,42")
        output_file = tmp_path / "output.parquet"

        # Use shell redirect to capture binary output to file
        import subprocess

        result = subprocess.run(
            f"uv run parquet-lf to-parquet csv {csv_file} > {output_file}",
            shell=True,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert output_file.exists()
        # Verify the redirected output is valid Parquet
        df = pl.read_parquet(output_file)
        assert df.shape == (1, 2)

    def test_csv_to_parquet_missing_file(self, run_cli, tmp_path: Path) -> None:
        """CLI returns error for missing input file."""
        nonexistent = tmp_path / "nonexistent.csv"

        result = run_cli(["to-parquet", "csv", str(nonexistent)])

        assert result.exit_code == 1
        assert "not found" in result.stderr.lower() or "error" in result.stderr.lower()


class TestToParquetNDJSON:
    """E2E tests for to-parquet ndjson command."""

    def test_ndjson_to_parquet_with_output_file(self, run_cli, tmp_path: Path) -> None:
        """CLI converts NDJSON to Parquet with -o flag."""
        ndjson_file = tmp_path / "input.ndjson"
        ndjson_file.write_text('{"name": "alice", "value": 10}\n{"name": "bob", "value": 20}')
        output_file = tmp_path / "output.parquet"

        result = run_cli(["to-parquet", "ndjson", str(ndjson_file), "-o", str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()
        df = pl.read_parquet(output_file)
        assert df.shape == (2, 2)

    def test_jsonl_alias_works(self, run_cli, tmp_path: Path) -> None:
        """CLI jsonl command is an alias for ndjson."""
        ndjson_file = tmp_path / "input.jsonl"
        ndjson_file.write_text('{"name": "test", "value": 42}')
        output_file = tmp_path / "output.parquet"

        result = run_cli(["to-parquet", "jsonl", str(ndjson_file), "-o", str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()

    def test_ndjson_to_parquet_missing_file(self, run_cli, tmp_path: Path) -> None:
        """CLI returns error for missing input file."""
        nonexistent = tmp_path / "nonexistent.ndjson"

        result = run_cli(["to-parquet", "ndjson", str(nonexistent)])

        assert result.exit_code == 1
        assert "not found" in result.stderr.lower() or "error" in result.stderr.lower()


class TestFromParquetCSV:
    """E2E tests for from-parquet csv command."""

    def test_parquet_to_csv_with_output_file(self, run_cli, tmp_path: Path) -> None:
        """CLI converts Parquet to CSV with -o flag."""
        parquet_file = tmp_path / "input.parquet"
        df = pl.DataFrame({"name": ["alice", "bob"], "value": [10, 20]})
        df.write_parquet(parquet_file)
        output_file = tmp_path / "output.csv"

        result = run_cli(["from-parquet", "csv", str(parquet_file), "-o", str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()
        content = output_file.read_text()
        assert "name,value" in content
        assert "alice" in content

    def test_parquet_to_csv_stdout(self, run_cli, tmp_path: Path) -> None:
        """CLI outputs CSV to stdout when no -o flag."""
        parquet_file = tmp_path / "input.parquet"
        df = pl.DataFrame({"name": ["test"], "value": [42]})
        df.write_parquet(parquet_file)

        result = run_cli(["from-parquet", "csv", str(parquet_file)])

        assert result.exit_code == 0
        assert "name,value" in result.stdout
        assert "test" in result.stdout

    def test_parquet_to_csv_missing_file(self, run_cli, tmp_path: Path) -> None:
        """CLI returns error for missing input file."""
        nonexistent = tmp_path / "nonexistent.parquet"

        result = run_cli(["from-parquet", "csv", str(nonexistent)])

        assert result.exit_code == 1
        assert "not found" in result.stderr.lower() or "error" in result.stderr.lower()


class TestFromParquetNDJSON:
    """E2E tests for from-parquet ndjson command."""

    def test_parquet_to_ndjson_with_output_file(self, run_cli, tmp_path: Path) -> None:
        """CLI converts Parquet to NDJSON with -o flag."""
        parquet_file = tmp_path / "input.parquet"
        df = pl.DataFrame({"name": ["alice", "bob"], "value": [10, 20]})
        df.write_parquet(parquet_file)
        output_file = tmp_path / "output.ndjson"

        result = run_cli(["from-parquet", "ndjson", str(parquet_file), "-o", str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()
        # Verify it's valid NDJSON
        read_df = pl.read_ndjson(output_file)
        assert read_df.shape == (2, 2)

    def test_parquet_to_ndjson_stdout(self, run_cli, tmp_path: Path) -> None:
        """CLI outputs NDJSON to stdout when no -o flag."""
        parquet_file = tmp_path / "input.parquet"
        df = pl.DataFrame({"name": ["test"], "value": [42]})
        df.write_parquet(parquet_file)

        result = run_cli(["from-parquet", "ndjson", str(parquet_file)])

        assert result.exit_code == 0
        assert "test" in result.stdout
        assert "42" in result.stdout

    def test_jsonl_alias_works(self, run_cli, tmp_path: Path) -> None:
        """CLI jsonl command is an alias for ndjson."""
        parquet_file = tmp_path / "input.parquet"
        df = pl.DataFrame({"name": ["test"], "value": [42]})
        df.write_parquet(parquet_file)
        output_file = tmp_path / "output.jsonl"

        result = run_cli(["from-parquet", "jsonl", str(parquet_file), "-o", str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()

    def test_parquet_to_ndjson_missing_file(self, run_cli, tmp_path: Path) -> None:
        """CLI returns error for missing input file."""
        nonexistent = tmp_path / "nonexistent.parquet"

        result = run_cli(["from-parquet", "ndjson", str(nonexistent)])

        assert result.exit_code == 1
        assert "not found" in result.stderr.lower() or "error" in result.stderr.lower()


class TestStdoutSeparation:
    """E2E tests verifying stdout/stderr separation."""

    def test_logs_go_to_stderr(self, run_cli, tmp_path: Path) -> None:
        """Logs are written to stderr, not stdout."""
        csv_file = tmp_path / "input.csv"
        csv_file.write_text("name,value\ntest,42")
        output_file = tmp_path / "output.parquet"

        result = run_cli(["to-parquet", "csv", str(csv_file), "-o", str(output_file)])

        assert result.exit_code == 0
        # Logs should be in stderr
        assert "conversion" in result.stderr.lower()
        # stdout should be empty when writing to file
        assert result.stdout == ""

    def test_data_goes_to_stdout(self, run_cli, tmp_path: Path) -> None:
        """Data output goes to stdout when no -o flag."""
        parquet_file = tmp_path / "input.parquet"
        df = pl.DataFrame({"name": ["test"], "value": [42]})
        df.write_parquet(parquet_file)

        result = run_cli(["from-parquet", "csv", str(parquet_file)])

        assert result.exit_code == 0
        # Data should be in stdout
        assert "name,value" in result.stdout
        # Logs should still be in stderr
        assert "conversion" in result.stderr.lower()


class TestInfoCommand:
    """E2E tests for the info command."""

    def test_info_parquet_shows_metadata(self, run_cli, tmp_path: Path) -> None:
        """Test info command shows metadata for Parquet file."""
        parquet_file = tmp_path / "test.parquet"
        df = pl.DataFrame({"name": ["alice", "bob"], "value": [1, 2]})
        df.write_parquet(parquet_file)

        result = run_cli(["info", str(parquet_file)])

        assert result.exit_code == 0
        assert "File: test.parquet" in result.stdout
        assert "Format: Parquet" in result.stdout
        assert "Rows: 2" in result.stdout
        assert "Columns: 2" in result.stdout
        assert "Schema:" in result.stdout
        assert "name: String" in result.stdout
        assert "value: Int64" in result.stdout

    def test_info_csv_shows_metadata(self, run_cli, tmp_path: Path) -> None:
        """Test info command shows metadata for CSV file."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,value\nalice,1\nbob,2")

        result = run_cli(["info", str(csv_file)])

        assert result.exit_code == 0
        assert "File: test.csv" in result.stdout
        assert "Format: Csv" in result.stdout
        assert "Rows: 2" in result.stdout

    def test_info_ndjson_shows_metadata(self, run_cli, tmp_path: Path) -> None:
        """Test info command shows metadata for NDJSON file."""
        ndjson_file = tmp_path / "test.ndjson"
        ndjson_file.write_text('{"name": "alice", "value": 1}\n{"name": "bob", "value": 2}')

        result = run_cli(["info", str(ndjson_file)])

        assert result.exit_code == 0
        assert "File: test.ndjson" in result.stdout
        assert "Format: Ndjson" in result.stdout
        assert "Rows: 2" in result.stdout

    def test_info_with_head_shows_preview(self, run_cli, tmp_path: Path) -> None:
        """Test info command with --head shows preview."""
        parquet_file = tmp_path / "test.parquet"
        df = pl.DataFrame({"name": ["alice", "bob", "charlie"], "value": [1, 2, 3]})
        df.write_parquet(parquet_file)

        result = run_cli(["info", "--head", "2", str(parquet_file)])

        assert result.exit_code == 0
        assert "Preview (first 2 rows):" in result.stdout
        assert "alice" in result.stdout
        assert "bob" in result.stdout

    def test_info_with_short_head_option(self, run_cli, tmp_path: Path) -> None:
        """Test info command with -n shorthand for --head."""
        parquet_file = tmp_path / "test.parquet"
        df = pl.DataFrame({"name": ["alice"], "value": [1]})
        df.write_parquet(parquet_file)

        result = run_cli(["info", "-n", "1", str(parquet_file)])

        assert result.exit_code == 0
        assert "Preview (first 1 rows):" in result.stdout

    def test_info_nonexistent_file_exits_with_error(self, run_cli, tmp_path: Path) -> None:
        """Test info command exits with code 1 for missing file."""
        nonexistent = tmp_path / "nonexistent.parquet"

        result = run_cli(["info", str(nonexistent)])

        assert result.exit_code == 1
        assert "Error:" in result.stderr
        assert "not found" in result.stderr.lower()

    def test_info_unsupported_extension_exits_with_error(self, run_cli, tmp_path: Path) -> None:
        """Test info command exits with code 1 for unsupported extension."""
        unsupported = tmp_path / "test.xyz"
        unsupported.write_text("some content")

        result = run_cli(["info", str(unsupported)])

        assert result.exit_code == 1
        assert "Error:" in result.stderr
        assert "Unsupported file extension" in result.stderr


class TestInfoWithExamples:
    """E2E tests using the example files in the examples/ directory."""

    def test_info_example_parquet(self, run_cli) -> None:
        """Test info command on examples/sample.parquet."""
        result = run_cli(["info", "examples/sample.parquet"])

        assert result.exit_code == 0
        assert "File: sample.parquet" in result.stdout
        assert "Format: Parquet" in result.stdout
        assert "Rows: 5" in result.stdout
        assert "Columns: 5" in result.stdout
        assert "id: Int64" in result.stdout
        assert "name: String" in result.stdout
        assert "age: Int64" in result.stdout
        assert "city: String" in result.stdout
        assert "score: Float64" in result.stdout

    def test_info_example_csv(self, run_cli) -> None:
        """Test info command on examples/sample.csv."""
        result = run_cli(["info", "examples/sample.csv"])

        assert result.exit_code == 0
        assert "File: sample.csv" in result.stdout
        assert "Format: Csv" in result.stdout
        assert "Rows: 5" in result.stdout

    def test_info_example_ndjson(self, run_cli) -> None:
        """Test info command on examples/sample.ndjson."""
        result = run_cli(["info", "examples/sample.ndjson"])

        assert result.exit_code == 0
        assert "File: sample.ndjson" in result.stdout
        assert "Format: Ndjson" in result.stdout
        assert "Rows: 5" in result.stdout

    def test_info_example_with_preview(self, run_cli) -> None:
        """Test info command with preview on example file."""
        result = run_cli(["info", "--head", "3", "examples/sample.parquet"])

        assert result.exit_code == 0
        assert "Preview (first 3 rows):" in result.stdout
        assert "Alice" in result.stdout
        assert "Bob" in result.stdout
        assert "Charlie" in result.stdout
