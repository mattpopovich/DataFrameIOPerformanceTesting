from formats.PickleFormat import PickleFormat
from formats.ParquetFormat import ParquetFormat
from formats.CsvFormat import CsvFormat


# TODO: Combine this with get_pickle_formats()
def get_csv_formats(verbose: bool, very_verbose) -> list[CsvFormat]:
    """
    Returns a list of CsvFormats containing compressions. If desired, also includes
    different compression levels.

    Args:
        verbose: True if you want different compression levels, False otherwise

    Returns:
        List of `CsvFormat`s
    """
    verbose = True if very_verbose else verbose

    formats: list[CsvFormat] = []
    formats.extend(
        CsvFormat(compression, compression_level)
        for compression in ["zip", "xz"]
        for compression_level in (list(range(0, 10)) + [None] if verbose else [None])
    )
    formats.extend(
        CsvFormat(compression, compression_level)
        for compression in ["gzip"]
        for compression_level in (list(range(-1, 10)) + [None] if verbose else [None])
    )  # Not sure why -1 works but we'll include it
    formats.extend(
        CsvFormat(compression, compression_level)
        for compression in ["bz2"]
        for compression_level in (list(range(1, 10)) + [None] if verbose else [None])
    )
    formats.extend(
        CsvFormat(compression, compression_level)
        for compression in ["zstd"]
        for compression_level in (list(range(-7, 23)) + [None] if verbose else [None])
    )
    formats.append(CsvFormat(None, None))

    # Test every read engine
    if very_verbose:
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


def get_pickle_formats(verbose: bool) -> list[PickleFormat]:
    """
    Returns a list of PickleFormats containing compressions. If desired, also includes
    different compression levels.

    Args:
        verbose: True if you want different compression levels, False otherwise

    Returns:
        List of `PickleFormat`s
    """
    formats: list[PickleFormat] = []
    formats.extend(
        PickleFormat(compression, compression_level)
        for compression in ["zip", "xz"]
        for compression_level in (list(range(0, 10)) + [None] if verbose else [None])
    )
    formats.extend(
        PickleFormat(compression, compression_level)
        for compression in ["gzip"]
        for compression_level in (list(range(-1, 10)) + [None] if verbose else [None])
    )  # Not sure why -1 works but we'll include it
    formats.extend(
        PickleFormat(compression, compression_level)
        for compression in ["bz2"]
        for compression_level in (list(range(1, 10)) + [None] if verbose else [None])
    )
    formats.extend(
        PickleFormat(compression, compression_level)
        for compression in ["zstd"]
        for compression_level in (list(range(-7, 23)) + [None] if verbose else [None])
    )
    formats.append(PickleFormat(None, None))
    return formats


def get_parquet_formats(verbose: bool) -> list[ParquetFormat]:
    """
    Returns a list of ParquetFormats containing compressions. If desired, also includes
    different parquet engines.

    Args:
        verbose: True if you want different parquet engines, False otherwise

    Returns:
        List of `ParquetFormat`s
    """
    formats: list[ParquetFormat] = []
    formats.extend(
        ParquetFormat(compression, write_engine, read_engine)
        for compression in [None, "snappy", "gzip", "brotli", "lz4", "zstd"]
        for write_engine in (["pyarrow", "fastparquet"] if verbose else ["auto"])
        for read_engine in (["pyarrow", "fastparquet"] if verbose else ["auto"])
    )
    return formats
