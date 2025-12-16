# parquet-lf

A lingua franca utility for converting between data formats (NDJSON, CSV) and Parquet.

## Installation

```bash
uv tool install parquet-lf
```

## Usage

### Convert to Parquet

```bash
# Convert CSV to Parquet
parquet-lf to-parquet csv input.csv -o output.parquet

# Convert NDJSON to Parquet
parquet-lf to-parquet ndjson input.ndjson -o output.parquet

# jsonl is an alias for ndjson
parquet-lf to-parquet jsonl input.jsonl -o output.parquet
```

### Convert from Parquet

```bash
# Convert Parquet to CSV
parquet-lf from-parquet csv input.parquet -o output.csv

# Convert Parquet to NDJSON
parquet-lf from-parquet ndjson input.parquet -o output.ndjson

# jsonl is an alias for ndjson
parquet-lf from-parquet jsonl input.parquet -o output.jsonl
```

### Output to stdout

When the `-o/--output` flag is omitted, output is written to stdout:

```bash
# Output CSV to stdout
parquet-lf from-parquet csv input.parquet

# Pipe to another command
parquet-lf from-parquet csv input.parquet | head -10

# Output Parquet to stdout (binary) and redirect to file
parquet-lf to-parquet csv input.csv > output.parquet
```

Note: Logs are written to stderr, so they won't interfere with piped data.

### Help

```bash
parquet-lf --help
parquet-lf to-parquet --help
parquet-lf from-parquet --help
```

## Supported Formats

### NDJSON (Newline Delimited JSON)

NDJSON is a format where each line is a valid JSON object. It's a true tabular peer to CSV, making it ideal for data interchange.

Example NDJSON file:
```json
{"name": "alice", "value": 10}
{"name": "bob", "value": 20}
{"name": "charlie", "value": 30}
```

Both `ndjson` and `jsonl` commands are supported as synonyms.

### CSV

Standard comma-separated values format with a header row.

Example CSV file:
```csv
name,value
alice,10
bob,20
charlie,30
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
