from utils import get_pickle_formats
from formats.PickleFormat import PickleFormat


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
