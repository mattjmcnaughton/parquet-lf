"""Info command handler with DTOs for input/output."""

from dataclasses import dataclass
from pathlib import Path

import polars as pl

from parquet_lf.info import (
    FileInfo,
    format_file_info,
    get_file_info,
    get_file_info_with_preview,
)


@dataclass
class InfoInput:
    """Input DTO for the info command."""

    input_file: Path
    head: int | None


@dataclass
class InfoOutput:
    """Output DTO for the info command."""

    file_info: FileInfo
    preview: pl.DataFrame | None
    formatted_output: str


def execute_info(input_dto: InfoInput) -> InfoOutput:
    """Execute the info command.

    Args:
        input_dto: Input DTO with file path and head option.

    Returns:
        InfoOutput DTO with file info, optional preview, and formatted output.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not supported.
    """
    if input_dto.head is not None:
        # Use optimized single-read path when preview is requested
        file_info, preview = get_file_info_with_preview(input_dto.input_file, input_dto.head)
    else:
        # Use lazy evaluation when no preview is needed
        file_info = get_file_info(input_dto.input_file)
        preview = None

    formatted_output = format_file_info(file_info, preview)

    return InfoOutput(
        file_info=file_info,
        preview=preview,
        formatted_output=formatted_output,
    )
