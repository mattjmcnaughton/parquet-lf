"""parquet-lf: A lingua franca utility for converting between data formats and Parquet."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("parquet-lf")
except PackageNotFoundError:
    __version__ = "0.0.0"
