# parquet-lf

A lingua franca utility for converting between data formats (JSON, CSV) and Parquet.

## Installation

```bash
uv tool install parquet-lf
```

## Usage

### Convert to Parquet

```bash
parquet-lf to-parquet json input.json -o output.parquet
parquet-lf to-parquet csv input.csv -o output.parquet
```

### Convert from Parquet

```bash
parquet-lf from-parquet json input.parquet -o output.json
parquet-lf from-parquet csv input.parquet -o output.csv
```

### Help

```bash
parquet-lf --help
parquet-lf to-parquet --help
parquet-lf from-parquet --help
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
