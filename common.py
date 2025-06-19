from PickleFormat import PickleFormat


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
