"""
Test utils.py
"""

import pytest

from utils import (
    get_pickle_formats,
    get_parquet_formats,
    get_csv_formats,
    get_compression_formats,
)
from config import list_of_compressions
from formats.PickleFormat import PickleFormat
from formats.ParquetFormat import ParquetFormat
from formats.CsvFormat import CsvFormat
from formats.BasicFormat import BasicFormat

NUM_COMPRESSIONS_WITH_LEVELS = (
    2 * (10 - 0 + 1) + (10 - -1 + 1) + (10 - 1 + 1) + (23 - -7 + 1) + 1
)  # 76
NUM_COMPRESSIONS = len(list_of_compressions)


def test_pickle_formats():
    formats = get_pickle_formats(False)
    assert all(
        isinstance(f, PickleFormat) for f in formats
    ), "Not all items are of type PickleFormat"
    assert len(formats) == NUM_COMPRESSIONS


def test_pickle_formats_with_compression_levels():
    formats = get_pickle_formats(True)
    assert all(
        isinstance(f, PickleFormat) for f in formats
    ), "Not all items are of type PickleFormat"
    assert len(formats) == NUM_COMPRESSIONS_WITH_LEVELS


def test_parquet_formats():
    formats = get_parquet_formats(False)
    assert all(
        isinstance(f, ParquetFormat) for f in formats
    ), "Not all items are of type ParquetFormat"
    assert (
        len(formats) == NUM_COMPRESSIONS
    ), f"Returned list contains {len(formats)} items"


def test_parquet_formats_with_engines():
    formats = get_parquet_formats(True)
    assert all(
        isinstance(f, ParquetFormat) for f in formats
    ), "Not all items are of type ParquetFormat"
    assert (
        len(formats) == NUM_COMPRESSIONS * 2 * 2  # Two read engines, two write engines
    ), f"Returned list contains {len(formats)} items"


def test_csv_formats():
    formats = get_csv_formats(False, False)
    assert all(
        isinstance(f, CsvFormat) for f in formats
    ), "Not all items are of type CsvFormat"
    assert len(formats) == NUM_COMPRESSIONS


def test_csv_formats_with_compression_levels():
    formats = get_csv_formats(True, False)
    assert all(
        isinstance(f, CsvFormat) for f in formats
    ), "Not all items are of type CsvFormat"
    assert len(formats) == NUM_COMPRESSIONS_WITH_LEVELS


def test_engine_csv_formats():
    formats = get_csv_formats(False, True)
    assert all(
        isinstance(f, CsvFormat) for f in formats
    ), "Not all items are of type CsvFormat"
    assert len(formats) == 3 * NUM_COMPRESSIONS


def test_compression_and_engine_csv_formats():
    formats = get_csv_formats(True, True)
    assert all(
        isinstance(f, CsvFormat) for f in formats
    ), "Not all items are of type CsvFormat"
    assert len(formats) == 3 * NUM_COMPRESSIONS_WITH_LEVELS  # 228


@pytest.mark.parametrize("formatType", [CsvFormat, PickleFormat])
def test_get_compression_formats(formatType: BasicFormat):
    formats = get_compression_formats(formatType, False)
    assert all(
        isinstance(f, formatType) for f in formats
    ), "Not all items are of the requested type"
    assert len(formats) == NUM_COMPRESSIONS


@pytest.mark.parametrize("formatType", [CsvFormat, PickleFormat])
def test_get_compression_formats_with_compression_levels(formatType: BasicFormat):
    formats = get_compression_formats(formatType, True)
    assert all(
        isinstance(f, formatType) for f in formats
    ), "Not all items are of the requested type"
    assert len(formats) == NUM_COMPRESSIONS_WITH_LEVELS
