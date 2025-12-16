"""From-parquet NDJSON command handler with DTOs for input/output."""

from dataclasses import dataclass
from pathlib import Path

from parquet_lf.converters.ndjson import parquet_to_ndjson


@dataclass
class FromParquetNdjsonInput:
    """Input DTO for the from-parquet ndjson command."""

    input_file: Path
    output: Path | None


def execute_from_parquet_ndjson(input_dto: FromParquetNdjsonInput) -> None:
    """Execute the from-parquet ndjson command.

    Args:
        input_dto: Input DTO with file path and output option.

    Raises:
        FileNotFoundError: If the input file does not exist.
        pl.exceptions.ComputeError: If the Parquet file cannot be read.
    """
    parquet_to_ndjson(input_dto.input_file, input_dto.output)
