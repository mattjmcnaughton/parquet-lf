"""CLI application for parquet-lf using Typer and structlog."""

import sys
from pathlib import Path
from typing import Annotated

import structlog
import typer

from parquet_lf import __version__
from parquet_lf.converters.csv import csv_to_parquet as convert_csv_to_parquet
from parquet_lf.converters.csv import parquet_to_csv as convert_parquet_to_csv
from parquet_lf.converters.ndjson import ndjson_to_parquet as convert_ndjson_to_parquet
from parquet_lf.converters.ndjson import parquet_to_ndjson as convert_parquet_to_ndjson

# Configure structlog for CLI usage
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=lambda *args: structlog.PrintLogger(file=sys.stderr),
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Main application
app = typer.Typer(
    name="parquet-lf",
    help="A lingua franca utility for converting between data formats and Parquet.",
    rich_markup_mode="markdown",
)

# Sub-application for to-parquet commands
to_parquet_app = typer.Typer(
    help="Convert files to Parquet format.",
)

# Sub-application for from-parquet commands
from_parquet_app = typer.Typer(
    help="Convert Parquet to other formats.",
)

# Register sub-applications
app.add_typer(to_parquet_app, name="to-parquet")
app.add_typer(from_parquet_app, name="from-parquet")


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        typer.echo(f"parquet-lf {__version__}")
        raise typer.Exit()


@app.callback()
def main_callback(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-v",
            help="Show version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """parquet-lf: Convert between data formats and Parquet."""
    pass


# --- to-parquet commands ---


def _handle_ndjson_to_parquet(input_file: Path, output: Path | None) -> None:
    """Shared handler for ndjson/jsonl to parquet conversion."""
    logger.info("conversion_start", direction="to_parquet", format="ndjson", input_file=str(input_file))
    try:
        convert_ndjson_to_parquet(input_file, output)
        logger.info("conversion_complete", direction="to_parquet", format="ndjson", input_file=str(input_file))
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.error("conversion_failed", direction="to_parquet", format="ndjson", error=str(e))
        typer.echo(f"Error: Failed to convert NDJSON to Parquet: {e}", err=True)
        raise typer.Exit(code=1) from None


@to_parquet_app.command("ndjson")
def ndjson_to_parquet(
    input_file: Annotated[
        Path,
        typer.Argument(help="Path to the input NDJSON file."),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Path to the output Parquet file."),
    ] = None,
) -> None:
    """Convert an NDJSON file to Parquet format."""
    _handle_ndjson_to_parquet(input_file, output)


@to_parquet_app.command("jsonl")
def jsonl_to_parquet(
    input_file: Annotated[
        Path,
        typer.Argument(help="Path to the input JSONL file."),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Path to the output Parquet file."),
    ] = None,
) -> None:
    """Convert a JSONL file to Parquet format (alias for ndjson)."""
    _handle_ndjson_to_parquet(input_file, output)


@to_parquet_app.command("csv")
def csv_to_parquet(
    input_file: Annotated[
        Path,
        typer.Argument(help="Path to the input CSV file."),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Path to the output Parquet file."),
    ] = None,
) -> None:
    """Convert a CSV file to Parquet format."""
    logger.info("conversion_start", direction="to_parquet", format="csv", input_file=str(input_file))
    try:
        convert_csv_to_parquet(input_file, output)
        logger.info("conversion_complete", direction="to_parquet", format="csv", input_file=str(input_file))
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.error("conversion_failed", direction="to_parquet", format="csv", error=str(e))
        typer.echo(f"Error: Failed to convert CSV to Parquet: {e}", err=True)
        raise typer.Exit(code=1) from None


# --- from-parquet commands ---


def _handle_parquet_to_ndjson(input_file: Path, output: Path | None) -> None:
    """Shared handler for parquet to ndjson/jsonl conversion."""
    logger.info("conversion_start", direction="from_parquet", format="ndjson", input_file=str(input_file))
    try:
        convert_parquet_to_ndjson(input_file, output)
        logger.info("conversion_complete", direction="from_parquet", format="ndjson", input_file=str(input_file))
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.error("conversion_failed", direction="from_parquet", format="ndjson", error=str(e))
        typer.echo(f"Error: Failed to convert Parquet to NDJSON: {e}", err=True)
        raise typer.Exit(code=1) from None


@from_parquet_app.command("ndjson")
def parquet_to_ndjson(
    input_file: Annotated[
        Path,
        typer.Argument(help="Path to the input Parquet file."),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Path to the output NDJSON file."),
    ] = None,
) -> None:
    """Convert a Parquet file to NDJSON format."""
    _handle_parquet_to_ndjson(input_file, output)


@from_parquet_app.command("jsonl")
def parquet_to_jsonl(
    input_file: Annotated[
        Path,
        typer.Argument(help="Path to the input Parquet file."),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Path to the output JSONL file."),
    ] = None,
) -> None:
    """Convert a Parquet file to JSONL format (alias for ndjson)."""
    _handle_parquet_to_ndjson(input_file, output)


@from_parquet_app.command("csv")
def parquet_to_csv(
    input_file: Annotated[
        Path,
        typer.Argument(help="Path to the input Parquet file."),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Path to the output CSV file."),
    ] = None,
) -> None:
    """Convert a Parquet file to CSV format."""
    logger.info("conversion_start", direction="from_parquet", format="csv", input_file=str(input_file))
    try:
        convert_parquet_to_csv(input_file, output)
        logger.info("conversion_complete", direction="from_parquet", format="csv", input_file=str(input_file))
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.error("conversion_failed", direction="from_parquet", format="csv", error=str(e))
        typer.echo(f"Error: Failed to convert Parquet to CSV: {e}", err=True)
        raise typer.Exit(code=1) from None
