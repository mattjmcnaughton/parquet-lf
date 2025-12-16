"""To-parquet CSV command handler with DTOs for input/output."""

from dataclasses import dataclass
from pathlib import Path

from parquet_lf.converters.csv import csv_to_parquet


@dataclass
class ToParquetCsvInput:
    """Input DTO for the to-parquet csv command."""

    input_file: Path
    output: Path | None


def execute_to_parquet_csv(input_dto: ToParquetCsvInput) -> None:
    """Execute the to-parquet csv command.

    Args:
        input_dto: Input DTO with file path and output option.

    Raises:
        FileNotFoundError: If the input file does not exist.
        pl.exceptions.ComputeError: If the CSV cannot be parsed.
    """
    csv_to_parquet(input_dto.input_file, input_dto.output)
