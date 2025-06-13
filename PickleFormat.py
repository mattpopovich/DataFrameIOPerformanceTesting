from BasicFormat import BasicFormat
import pandas as pd


class PickleFormat(BasicFormat):
    """
    Implements reading and writing of Pandas DataFrames in the Pickle format
    """

    def __init__(self, compression: str | None):
        super().__init__(extension="pkl")
        self._compression = compression
        # The compression type is zstd but the file extension is zst
        self._compression_extension = "zst" if compression == "zstd" else compression

        # Add compression to file path (if necessary)
        self._compression_path = "." + self._compression_extension if compression else ""
        self.file_path += self._compression_path

    def __str__(self):
        return self._extension + self._compression_path

    def write(self, df: pd.DataFrame) -> None:
        # TODO: Specify compresslevel

        # .to_pickle will detect compression based on the path given
        #   https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_pickle.html#pandas.DataFrame.to_pickle
        df.to_pickle(self.file_path)

    def read(self):
        # .read_pickle will detect compression based on the path given
        #   https://pandas.pydata.org/docs/reference/api/pandas.read_pickle.html#pandas.read_pickle
        return pd.read_pickle(self.file_path)
