from formats.AdvancedFormat import AdvancedFormat
import pandas as pd


class PickleFormat(AdvancedFormat):
    """
    Implements reading and writing of Pandas DataFrames in the Pickle format

    compression_level can only be supplied for compressions: [zip, gzip, bz2, zstd, xz]
    """

    def __init__(self, compression: str | None, compression_level: int | None):
        super().__init__(
            extension="pkl", compression=compression, compression_level=compression_level
        )

    def __str__(self) -> str:
        return self._extension + self._compression_path + self.compression_level_str

    def write(self, df: pd.DataFrame) -> None:
        if self._compression_level:
            # Dictionary is required if we want to specify compression level
            df.to_pickle(self.file_path, compression=self.compression_dict)
        else:
            # .to_pickle will detect compression type based on the path given
            #   https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_pickle.html#pandas.DataFrame.to_pickle
            df.to_pickle(self.file_path)

    def read(self):
        # .read_pickle will detect compression type based on the path given
        #   (but not always compression level)
        #   https://pandas.pydata.org/docs/reference/api/pandas.read_pickle.html#pandas.read_pickle

        if (
            self._compression == "gzip"
            and self._compression_level != None
            and self._compression_level != 0
        ):
            # Dictionary is required if we want to specify compression level
            return pd.read_pickle(self.file_path, compression=self.compression_dict)
        else:
            # .to_pickle will detect compression type based on the path given
            #   https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_pickle.html#pandas.DataFrame.to_pickle
            return pd.read_pickle(self.file_path)
