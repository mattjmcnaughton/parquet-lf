# parquet-lf development commands

# Install all dependencies including dev group
install:
    uv sync --group dev

# Run parquet-lf CLI
dev *ARGS:
    uv run parquet-lf {{ARGS}}

# Run ruff linter
lint:
    uv run ruff check .

# Run ruff linter with auto-fix
lint-fix:
    uv run ruff check . --fix

# Run ruff formatter
format:
    uv run ruff format .

# Check formatting without making changes
format-check:
    uv run ruff format --check .

# Run ty type checker
typecheck:
    uv run ty check

# Run all tests
test:
    uv run pytest

# Run unit tests only
test-unit:
    uv run pytest tests/unit/

# Run integration tests only
test-integration:
    uv run pytest tests/integration/

# Run end-to-end tests only
test-e2e:
    uv run pytest tests/e2e/

# Run full CI pipeline (lint, format check, typecheck, test)
ci: lint format-check typecheck test
