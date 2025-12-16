"""From-parquet CSV command handler with DTOs for input/output."""

from dataclasses import dataclass
from pathlib import Path

from parquet_lf.converters.csv import parquet_to_csv


@dataclass
class FromParquetCsvInput:
    """Input DTO for the from-parquet csv command."""

    input_file: Path
    output: Path | None


def execute_from_parquet_csv(input_dto: FromParquetCsvInput) -> None:
    """Execute the from-parquet csv command.

    Args:
        input_dto: Input DTO with file path and output option.

    Raises:
        FileNotFoundError: If the input file does not exist.
        pl.exceptions.ComputeError: If the Parquet file cannot be read.
    """
    parquet_to_csv(input_dto.input_file, input_dto.output)
