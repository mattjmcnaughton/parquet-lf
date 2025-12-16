"""To-parquet NDJSON command handler with DTOs for input/output."""

from dataclasses import dataclass
from pathlib import Path

from parquet_lf.converters.ndjson import ndjson_to_parquet


@dataclass
class ToParquetNdjsonInput:
    """Input DTO for the to-parquet ndjson command."""

    input_file: Path
    output: Path | None


def execute_to_parquet_ndjson(input_dto: ToParquetNdjsonInput) -> None:
    """Execute the to-parquet ndjson command.

    Args:
        input_dto: Input DTO with file path and output option.

    Raises:
        FileNotFoundError: If the input file does not exist.
        pl.exceptions.ComputeError: If the NDJSON cannot be parsed.
    """
    ndjson_to_parquet(input_dto.input_file, input_dto.output)
