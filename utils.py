"""
Various functions that are helpful to analyze_dataframe_io.py
"""

from formats.PickleFormat import PickleFormat
from formats.ParquetFormat import ParquetFormat
from formats.CsvFormat import CsvFormat
from formats.BasicFormat import BasicFormat


def get_compression_formats(
    formatType: BasicFormat, compression_levels: bool
) -> list[BasicFormat]:
    """
    Given a formatType, will return a list of formatTypes that contains all compressions
    (and compression levels, if desired).

    Args:
        formatType: The BasicFormat that the returned list will contain
        compression_levels: True if you want different compression levels, False otherwise

    Returns:
        List of `formatType`s
    """
    formats: list[BasicFormat] = []
    formats.extend(
        formatType(compression, compression_level)
        for compression in ["zip", "xz"]
        for compression_level in (
            list(range(0, 10)) + [None] if compression_levels else [None]
        )
    )
    formats.extend(
        formatType(compression, compression_level)
        for compression in ["gzip"]
        for compression_level in (
            list(range(-1, 10)) + [None] if compression_levels else [None]
        )
    )  # Not sure why -1 works but we'll include it
    formats.extend(
        formatType(compression, compression_level)
        for compression in ["bz2"]
        for compression_level in (
            list(range(1, 10)) + [None] if compression_levels else [None]
        )
    )
    formats.extend(
        formatType(compression, compression_level)
        for compression in ["zstd"]
        for compression_level in (
            list(range(-7, 23)) + [None] if compression_levels else [None]
        )
    )
    formats.append(formatType(None, None))

    return formats


def get_csv_formats(compression_levels: bool, read_engines: bool) -> list[CsvFormat]:
    """
    Returns a list of CsvFormats containing compressions. If desired, also includes
    different compression levels.

    Args:
        compression_levels: True if you want different compression levels, False otherwise
        read_engines: True if you want to test every read engine, False otherwise

    Returns:
        List of `CsvFormat`s
    """
    formats: list[CsvFormat] = get_compression_formats(CsvFormat, compression_levels)

    # Test every read engine
    if read_engines:
        formats_with_engines: list[CsvFormat] = []
        for f in formats:
            for engine in ["c", "python", "pyarrow"]:
                # pyarrow >> c >> python in tests I've done. Each are about 3x faster than the other
                formats_with_engines.append(
                    CsvFormat(f._compression, f._compression_level, engine)
                )
        return formats_with_engines
    else:
        return formats


def get_pickle_formats(compression_levels: bool) -> list[PickleFormat]:
    """
    Returns a list of PickleFormats containing compressions. If desired, also includes
    different compression levels.

    Args:
        compression_levels: True if you want different compression levels, False otherwise

    Returns:
        List of `PickleFormat`s
    """
    formats: list[PickleFormat] = get_compression_formats(
        PickleFormat, compression_levels
    )
    return formats


def get_parquet_formats(include_engines: bool) -> list[ParquetFormat]:
    """
    Returns a list of ParquetFormats containing compressions. If desired, also includes
    different parquet engines.

    Args:
        include_engines: True if you want different parquet engines, False otherwise

    Returns:
        List of `ParquetFormat`s
    """
    formats: list[ParquetFormat] = []
    formats.extend(
        ParquetFormat(compression, write_engine, read_engine)
        for compression in [None, "snappy", "gzip", "brotli", "lz4", "zstd"]
        for write_engine in (["pyarrow", "fastparquet"] if include_engines else ["auto"])
        for read_engine in (["pyarrow", "fastparquet"] if include_engines else ["auto"])
    )
    return formats
