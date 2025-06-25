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
from formats.PickleFormat import PickleFormat
from formats.ParquetFormat import ParquetFormat
from formats.CsvFormat import CsvFormat
from formats.BasicFormat import BasicFormat

NUM_COMPRESSION_TESTS = (
    2 * (10 - 0 + 1) + (10 - -1 + 1) + (10 - 1 + 1) + (23 - -7 + 1) + 1
)  # 76


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
    assert len(formats) == NUM_COMPRESSION_TESTS


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
    formats = get_csv_formats(False, False)
    assert all(
        isinstance(f, CsvFormat) for f in formats
    ), "Not all items are of type CsvFormat"
    assert len(formats) == 6


def test_verbose_csv_formats():
    formats = get_csv_formats(True, False)
    assert all(
        isinstance(f, CsvFormat) for f in formats
    ), "Not all items are of type CsvFormat"
    assert len(formats) == NUM_COMPRESSION_TESTS


@pytest.mark.parametrize(
    "verbose",
    [
        True,
        False,
    ],
)
def test_very_verbose_csv_formats(verbose: bool):
    formats = get_csv_formats(verbose, True)
    assert all(
        isinstance(f, CsvFormat) for f in formats
    ), "Not all items are of type CsvFormat"
    assert len(formats) == 3 * NUM_COMPRESSION_TESTS  # 228


@pytest.mark.parametrize("formatType", [CsvFormat, PickleFormat])
def test_get_compression_formats(formatType: BasicFormat):
    formats = get_compression_formats(formatType, False)
    assert all(
        isinstance(f, formatType) for f in formats
    ), "Not all items are of the requested type"
    assert len(formats) == 6


@pytest.mark.parametrize("formatType", [CsvFormat, PickleFormat])
def test_get_compression_formats_verbose(formatType: BasicFormat):
    formats = get_compression_formats(formatType, True)
    assert all(
        isinstance(f, formatType) for f in formats
    ), "Not all items are of the requested type"
    assert len(formats) == NUM_COMPRESSION_TESTS
