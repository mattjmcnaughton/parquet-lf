"""Info module for file inspection and metadata retrieval."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import polars as pl


class FileFormat(Enum):
    """Supported file formats for the info command."""

    PARQUET = "parquet"
    CSV = "csv"
    NDJSON = "ndjson"


# Map file extensions to formats
EXTENSION_MAP: dict[str, FileFormat] = {
    ".parquet": FileFormat.PARQUET,
    ".csv": FileFormat.CSV,
    ".ndjson": FileFormat.NDJSON,
    ".jsonl": FileFormat.NDJSON,
}

# Size formatting constants
BYTES_PER_KB = 1024
BYTES_PER_MB = BYTES_PER_KB * 1024
BYTES_PER_GB = BYTES_PER_MB * 1024


def detect_format(path: Path) -> FileFormat:
    """Detect file format from extension.

    Args:
        path: Path to the file.

    Returns:
        FileFormat enum value.

    Raises:
        ValueError: If the file extension is not supported.
    """
    ext = path.suffix.lower()
    if ext not in EXTENSION_MAP:
        raise ValueError(f"Unsupported file extension: {ext}")
    return EXTENSION_MAP[ext]


@dataclass
class FileInfo:
    """Container for file metadata."""

    path: Path
    format: FileFormat
    size_bytes: int
    row_count: int
    column_count: int
    schema: dict[str, str]


def _read_file(path: Path, file_format: FileFormat) -> pl.DataFrame:
    """Read a file into a DataFrame based on format.

    Args:
        path: Path to the file.
        file_format: The format of the file.

    Returns:
        DataFrame with file contents.
    """
    match file_format:
        case FileFormat.PARQUET:
            return pl.read_parquet(path)
        case FileFormat.CSV:
            return pl.read_csv(path)
        case FileFormat.NDJSON:
            return pl.read_ndjson(path)


def _get_row_count_lazy(path: Path, file_format: FileFormat) -> int:
    """Get row count using lazy evaluation when possible.

    Args:
        path: Path to the file.
        file_format: The format of the file.

    Returns:
        Number of rows in the file.
    """
    match file_format:
        case FileFormat.PARQUET:
            # Use lazy scanning to count rows without loading all data
            return pl.scan_parquet(path).select(pl.len()).collect().item()
        case FileFormat.CSV:
            return pl.scan_csv(path).select(pl.len()).collect().item()
        case FileFormat.NDJSON:
            return pl.scan_ndjson(path).select(pl.len()).collect().item()


def _get_schema(path: Path, file_format: FileFormat) -> dict[str, str]:
    """Get schema from a file using lazy evaluation when possible.

    Args:
        path: Path to the file.
        file_format: The format of the file.

    Returns:
        Dict mapping column names to type strings.
    """
    match file_format:
        case FileFormat.PARQUET:
            schema = pl.scan_parquet(path).collect_schema()
        case FileFormat.CSV:
            schema = pl.scan_csv(path).collect_schema()
        case FileFormat.NDJSON:
            schema = pl.scan_ndjson(path).collect_schema()

    return {name: str(dtype) for name, dtype in schema.items()}


def get_file_info(path: Path) -> FileInfo:
    """Get metadata about a file.

    Uses lazy evaluation to avoid loading the entire file into memory.

    Args:
        path: Path to the file.

    Returns:
        FileInfo dataclass with file metadata.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not supported.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    file_format = detect_format(path)
    size_bytes = path.stat().st_size

    # Get schema and row count using lazy evaluation
    schema_dict = _get_schema(path, file_format)
    row_count = _get_row_count_lazy(path, file_format)

    return FileInfo(
        path=path,
        format=file_format,
        size_bytes=size_bytes,
        row_count=row_count,
        column_count=len(schema_dict),
        schema=schema_dict,
    )


def get_file_info_with_preview(path: Path, head: int) -> tuple[FileInfo, pl.DataFrame]:
    """Get metadata and preview in a single file read.

    This is more efficient than calling get_file_info() separately
    when a preview is needed.

    Args:
        path: Path to the file.
        head: Number of rows to include in preview.

    Returns:
        Tuple of (FileInfo, preview DataFrame).

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not supported.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    file_format = detect_format(path)
    size_bytes = path.stat().st_size

    # Read the file once
    df = _read_file(path, file_format)

    # Extract schema from the loaded DataFrame
    schema_dict = {name: str(dtype) for name, dtype in df.schema.items()}

    file_info = FileInfo(
        path=path,
        format=file_format,
        size_bytes=size_bytes,
        row_count=df.shape[0],
        column_count=df.shape[1],
        schema=schema_dict,
    )

    preview = df.head(head)

    return file_info, preview


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes.

    Returns:
        Formatted size string (e.g., "1.2 KB", "3.5 MB").
    """
    if size_bytes < BYTES_PER_KB:
        return f"{size_bytes} B"
    elif size_bytes < BYTES_PER_MB:
        return f"{size_bytes / BYTES_PER_KB:.1f} KB"
    elif size_bytes < BYTES_PER_GB:
        return f"{size_bytes / BYTES_PER_MB:.1f} MB"
    else:
        return f"{size_bytes / BYTES_PER_GB:.1f} GB"


def format_file_info(info: FileInfo, preview: pl.DataFrame | None = None) -> str:
    """Format file info as human-readable text.

    Args:
        info: FileInfo dataclass with metadata.
        preview: Optional DataFrame with preview rows.

    Returns:
        Formatted string for display.
    """
    lines = [
        f"File: {info.path.name}",
        f"Format: {info.format.value.capitalize()}",
        f"Size: {format_size(info.size_bytes)}",
        f"Rows: {info.row_count}",
        f"Columns: {info.column_count}",
        "",
        "Schema:",
    ]

    for name, dtype in info.schema.items():
        lines.append(f"  {name}: {dtype}")

    if preview is not None:
        lines.append("")
        lines.append(f"Preview (first {len(preview)} rows):")
        lines.append(str(preview))

    return "\n".join(lines)
