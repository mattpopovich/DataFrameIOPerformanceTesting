from utils import get_pickle_formats, get_parquet_formats, get_csv_formats
from formats.PickleFormat import PickleFormat
from formats.ParquetFormat import ParquetFormat
from formats.CsvFormat import CsvFormat


def test_pickle_formats():
    formats = get_pickle_formats(False)
    assert all(
        isinstance(f, PickleFormat) for f in formats
    ), "Not all items are of type PickleFormat"
    assert len(formats) == 6


def test_verbose_pickle_formats():
    formats = get_pickle_formats(True)
    assert all(
        isinstance(f, PickleFormat) for f in formats
    ), "Not all items are of type PickleFormat"
    assert (
        len(formats)
        == 2 * (10 - 0 + 1) + (10 - -1 + 1) + (10 - 1 + 1) + (23 - -7 + 1) + 1
    )


def test_parquet_formats():
    formats = get_parquet_formats(False)
    assert all(
        isinstance(f, ParquetFormat) for f in formats
    ), "Not all items are of type ParquetFormat"
    assert len(formats) == 6, f"Returned list contains {len(formats)} items"


def test_verbose_parquet_formats():
    formats = get_parquet_formats(True)
    assert all(
        isinstance(f, ParquetFormat) for f in formats
    ), "Not all items are of type ParquetFormat"
    assert len(formats) == 6 * 2 * 2, f"Returned list contains {len(formats)} items"


def test_csv_formats():
    formats = get_csv_formats(False)
    assert all(
        isinstance(f, CsvFormat) for f in formats
    ), "Not all items are of type CsvFormat"
    assert len(formats) == 6


def test_verbose_csv_formats():
    formats = get_csv_formats(True)
    assert all(
        isinstance(f, CsvFormat) for f in formats
    ), "Not all items are of type CsvFormat"
    assert (
        len(formats)
        == 2 * (10 - 0 + 1) + (10 - -1 + 1) + (10 - 1 + 1) + (23 - -7 + 1) + 1
    )
