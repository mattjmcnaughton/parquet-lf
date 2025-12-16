"""CLI application for parquet-lf using Typer and structlog."""

import sys
from pathlib import Path
from typing import Annotated

import structlog
import typer

from parquet_lf import __version__

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


@to_parquet_app.command("json")
def json_to_parquet(
    input_file: Annotated[
        Path,
        typer.Argument(help="Path to the input JSON file."),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Path to the output Parquet file."),
    ] = None,
) -> None:
    """Convert a JSON file to Parquet format."""
    logger.info("not_implemented", command="to-parquet json", input_file=str(input_file))
    typer.echo("Error: JSON to Parquet conversion is not yet implemented.", err=True)
    raise typer.Exit(code=1)


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
    logger.info("not_implemented", command="to-parquet csv", input_file=str(input_file))
    typer.echo("Error: CSV to Parquet conversion is not yet implemented.", err=True)
    raise typer.Exit(code=1)


# --- from-parquet commands ---


@from_parquet_app.command("json")
def parquet_to_json(
    input_file: Annotated[
        Path,
        typer.Argument(help="Path to the input Parquet file."),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Path to the output JSON file."),
    ] = None,
) -> None:
    """Convert a Parquet file to JSON format."""
    logger.info("not_implemented", command="from-parquet json", input_file=str(input_file))
    typer.echo("Error: Parquet to JSON conversion is not yet implemented.", err=True)
    raise typer.Exit(code=1)


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
    logger.info("not_implemented", command="from-parquet csv", input_file=str(input_file))
    typer.echo("Error: Parquet to CSV conversion is not yet implemented.", err=True)
    raise typer.Exit(code=1)
