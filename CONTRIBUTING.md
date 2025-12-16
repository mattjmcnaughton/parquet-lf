# Contributing to parquet-lf

Thank you for your interest in contributing to parquet-lf!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/mattjmcnaughton/parquet-lf.git
   cd parquet-lf
   ```

2. Install dependencies using uv:
   ```bash
   just install
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

Run `just --list` to see all available development commands.

Run `just ci` to run all checks (linting, formatting, type checking, tests).

## Code Style

- Line length: 120 characters
- Use absolute imports
- Follow PEP 8 conventions (enforced by ruff)
- Use type hints for all function signatures
- Use structlog for logging with snake_case event names

## Commit Conventions

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for semantic versioning:

- `fix:` - Bug fixes (triggers PATCH version bump)
- `feat:` - New features (triggers MINOR version bump)
- `BREAKING CHANGE:` - Breaking changes (triggers MAJOR version bump)

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all checks pass: `just ci`
4. Submit a pull request to `main`
5. Wait for review and address any feedback
