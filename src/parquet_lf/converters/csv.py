"""CSV to/from Parquet converter."""

from pathlib import Path

import polars as pl

from parquet_lf.converters.base import write_parquet_output, write_text_output


def csv_to_parquet(input_path: Path, output: Path | None) -> None:
    """Convert CSV file to Parquet format.

    Args:
        input_path: Path to the input CSV file.
        output: Output path, or None/"-" for stdout.

    Raises:
        FileNotFoundError: If the input file does not exist.
        pl.exceptions.ComputeError: If the CSV cannot be parsed.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pl.read_csv(input_path)
    write_parquet_output(df, output)


def parquet_to_csv(input_path: Path, output: Path | None) -> None:
    """Convert Parquet file to CSV format.

    Args:
        input_path: Path to the input Parquet file.
        output: Output path, or None/"-" for stdout.

    Raises:
        FileNotFoundError: If the input file does not exist.
        pl.exceptions.ComputeError: If the Parquet file cannot be read.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pl.read_parquet(input_path)

    if output is None or str(output) == "-":
        content = df.write_csv()
        write_text_output(content, output)
    else:
        df.write_csv(output)
