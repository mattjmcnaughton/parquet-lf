# CLAUDE.md - Project Guidance for AI Assistants

This file captures project-specific conventions and guidance for AI coding assistants working on parquet-lf.

## Project Overview

parquet-lf is a CLI tool for bidirectional conversion between Parquet and tabular formats (CSV, NDJSON). It uses Polars for data processing and Typer for the CLI interface.

## Code Style

### Imports

- Use **absolute imports only** (e.g., `from parquet_lf.converters.base import ...`)
- No relative imports (avoid `from .base import ...`)
- Keep `__init__.py` files minimal - do not re-export or aggregate imports
- Import order is enforced by ruff (stdlib, third-party, local)

### Type Hints

- All function signatures must have type hints
- Use `Path | None` union syntax (Python 3.10+ style), not `Optional[Path]`
- Type checker: `ty` (run with `uv run ty check src/`)

### Error Handling

- Use `raise typer.Exit(code=1) from None` in except blocks (ruff B904 requires `from None` or `from err`)
- Prefer explicit `FileNotFoundError` checks over catching generic exceptions

### Logging

- Use structlog with snake_case event names
- Logs go to stderr (preserves stdout for data output)
- Log conversion start/complete events

## Testing Organization

### Test Layers

```
tests/
  unit/           # Pure logic tests, no filesystem or external dependencies
  integration/    # Tests that touch filesystem, databases, or external services
  e2e/            # Full CLI invocation tests
```

### What Goes Where

**Unit tests (`tests/unit/`):**
- Test pure functions and logic in isolation
- Use in-memory data fixtures (strings, dicts, DataFrames)
- No filesystem operations (no `tmp_path` for test data files)
- Mock external dependencies if needed

**Integration tests (`tests/integration/`):**
- Test components working together
- File-based fixtures belong here (use `tmp_path`)
- Round-trip conversion tests
- Hypothesis property-based tests with file I/O

**E2E tests (`tests/e2e/`):**
- Test full CLI invocation via subprocess or CLI runner
- Use the `run_cli` fixture from `tests/e2e/conftest.py`
- Verify exit codes, stdout/stderr output
- For binary stdout (Parquet), use shell redirects instead of `text=True`

### Running Tests

```bash
uv run pytest                    # All tests
uv run pytest tests/unit/        # Unit only
uv run pytest tests/integration/ # Integration only
uv run pytest tests/e2e/         # E2E only
uv run pytest -v                 # Verbose output
```

## Dependencies

### Core Dependencies

- **polars >= 1.36.1**: Data processing library (multi-threaded, Arrow-native)
- **typer >= 0.17.4**: CLI framework
- **structlog >= 25.4.0**: Structured logging

### Dev Dependencies

- **pytest**: Test framework
- **hypothesis**: Property-based testing
- **ruff**: Linting and formatting
- **ty**: Type checking

## Linting and Formatting

```bash
uv run ruff check src/ tests/    # Lint
uv run ruff format src/ tests/   # Format
uv run ty check src/             # Type check
```

Ruff rules enabled: E, F, I, B, UP (see pyproject.toml)

## CLI Architecture

- Two command groups: `to-parquet` and `from-parquet`
- Each format has its own subcommand (csv, ndjson, jsonl)
- `jsonl` is an alias for `ndjson`
- Output to stdout when `-o` is omitted or set to `-`
- Binary output (Parquet) uses `sys.stdout.buffer`

## Command Module Pattern

Commands use a DTO (Data Transfer Object) pattern with Input/Output dataclasses:

```
src/parquet_lf/command/
  __init__.py           # Empty, no re-exports
  info.py               # InfoInput, InfoOutput, execute_info()
  to_parquet_csv.py     # ToParquetCsvInput, ToParquetCsvOutput, execute_to_parquet_csv()
  from_parquet_csv.py   # etc.
```

### Structure for New Commands

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MyCommandInput:
    input_file: Path
    option: str | None = None

@dataclass
class MyCommandOutput:
    result: str
    # Add fields as needed

def execute_my_command(input_data: MyCommandInput) -> MyCommandOutput:
    # Business logic here, no CLI concerns
    return MyCommandOutput(result="...")
```

### Benefits

- CLI layer (`cli.py`) handles parsing, logging, error handling
- Command modules contain pure business logic
- DTOs make testing easier (construct Input, assert on Output)
- Clear separation of concerns

## Demo Data

Demo files are in `examples/` directory:
- `examples/sample.parquet`
- `examples/sample.csv`
- `examples/sample.ndjson`

Regenerate with: `uv run python scripts/generate_examples.py`
