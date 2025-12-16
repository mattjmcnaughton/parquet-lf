"""Base utilities for format converters."""

import io
import sys
from pathlib import Path

import polars as pl


def write_parquet_output(df: pl.DataFrame, output: Path | None) -> None:
    """Write DataFrame to Parquet file or stdout.

    Args:
        df: The Polars DataFrame to write.
        output: Output path, or None/"-" for stdout.
    """
    if output is None or str(output) == "-":
        buffer = io.BytesIO()
        df.write_parquet(buffer)
        buffer.seek(0)
        sys.stdout.buffer.write(buffer.read())
    else:
        df.write_parquet(output)


def write_text_output(content: str, output: Path | None) -> None:
    """Write text content to file or stdout.

    Args:
        content: The text content to write.
        output: Output path, or None/"-" for stdout.
    """
    if output is None or str(output) == "-":
        sys.stdout.write(content)
    else:
        output.write_text(content)
