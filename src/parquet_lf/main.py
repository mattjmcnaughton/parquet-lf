"""Entry point for the parquet-lf CLI."""

from parquet_lf.cli import app


def main() -> None:
    """Run the parquet-lf CLI application."""
    app()


if __name__ == "__main__":
    main()
