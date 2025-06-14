from BasicFormat import BasicFormat
import pandas as pd


class PickleFormat(BasicFormat):
    """
    Implements reading and writing of Pandas DataFrames in the Pickle format
    """

    def __init__(self, compression: str | None, compression_level: int):
        super().__init__(extension="pkl")
        self._compression = compression
        self._compression_extension = self._compression
        self._compression_level = compression_level

        # The compression type is zstd but the file extension is zst
        self._compression_extension = "zst" if compression == "zstd" else compression

        # Add compression to file path (if necessary)
        self._compression_path = "." + self._compression_extension if compression else ""
        self.file_path += self._compression_path

    def __str__(self):
        return (
            self._extension
            + self._compression_path
            + " CL"
            + str(self._compression_level)
        )

    def write(self, df: pd.DataFrame) -> None:
        """
        zip = compresslevel: -1 - 9
        gzip = compresslevel: -1 - 9
        bz2 = compresslevel: 1 - 9
        zstd = level: -7 - 22
        xz = preset: 0 - 9
        tar = just archives, not compresses
        """
        if self._compression_level:
            # Dictionary is required if we want to specify compression level
            compression_dict = {
                "method": self._compression,
                "level": self._compression_level,
            }
            df.to_pickle(self.file_path, compression=compression_dict)
        else:
            # .to_pickle will detect compression type based on the path given
            #   https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_pickle.html#pandas.DataFrame.to_pickle
            df.to_pickle(self.file_path)

    def read(self):
        """
        Sometimes you have to specify the compression level when reading

        zip = specify or no specify
        gzip = specify
        bz2 = specify or no specify
        zstd = no specify
        xz = no specify
        tar =
        """
        # .read_pickle will detect compression based on the path given
        #   https://pandas.pydata.org/docs/reference/api/pandas.read_pickle.html#pandas.read_pickle

        # if self._compression_level:
        #     # Dictionary is required if we want to specify compression level
        #     compression_dict = {
        #         "method": self._compression,
        #         "compresslevel": self._compression_level,
        #     }
        #     return pd.read_pickle(self.file_path, compression=compression_dict)
        # else:
        #     # .to_pickle will detect compression type based on the path given
        #     #   https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_pickle.html#pandas.DataFrame.to_pickle
        #     return pd.read_pickle(self.file_path)

        return pd.read_pickle(self.file_path)
