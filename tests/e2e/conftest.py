"""Fixtures for end-to-end CLI tests."""

import subprocess
from typing import NamedTuple

import pytest


class CLIResult(NamedTuple):
    """Result from running a CLI command."""

    exit_code: int
    stdout: str
    stderr: str


@pytest.fixture
def run_cli():
    """Fixture that returns a function to run parquet-lf CLI commands.

    Usage:
        result = run_cli(["--help"])
        assert result.exit_code == 0
    """

    def _run_cli(args: list[str], input_text: str | None = None) -> CLIResult:
        """Run parquet-lf with the given arguments.

        Args:
            args: Command line arguments to pass to parquet-lf.
            input_text: Optional text to pass to stdin.

        Returns:
            CLIResult with exit_code, stdout, and stderr.
        """
        result = subprocess.run(
            ["uv", "run", "parquet-lf", *args],
            capture_output=True,
            text=True,
            input=input_text,
        )
        return CLIResult(
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )

    return _run_cli
