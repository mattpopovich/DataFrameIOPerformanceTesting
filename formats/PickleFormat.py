from formats.BasicFormat import BasicFormat
import pandas as pd


class PickleFormat(BasicFormat):
    """
    Implements reading and writing of Pandas DataFrames in the Pickle format

    compression_level can only be supplied for compressions: [zip, gzip, bz2, zstd, xz]
    """

    def __init__(self, compression: str | None, compression_level: int | None):
        super().__init__(extension="pkl")
        if compression_level != None:
            self.file_path = f"{self._folder_name}/{self._file_name}C{compression_level}.{self._extension}"
        self._compression = compression
        # The compression type is zstd but the file extension is zst
        self._compression_extension = "zst" if compression == "zstd" else compression
        self._compression_level = compression_level

        # Add compression to file path (if necessary)
        self._compression_path = "." + self._compression_extension if compression else ""
        self.file_path += self._compression_path

        # Thanks, pandas, for making these different
        if self._compression == "xz":
            self._compression_key = "preset"
        elif self._compression == "zstd":
            self._compression_key = "level"
        else:
            self._compression_key = "compresslevel"

    def __str__(self):
        compression_level_str = (
            " C=" + str(self._compression_level)
            if self._compression_level != None
            else ""
        )
        return self._extension + self._compression_path + compression_level_str

    def write(self, df: pd.DataFrame) -> None:
        """
        zip = compresslevel: 0 - 9 : https://docs.python.org/3/library/gzip.html
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
                self._compression_key: self._compression_level,
            }
            df.to_pickle(self.file_path, compression=compression_dict)
        else:
            # .to_pickle will detect compression type based on the path given
            #   https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_pickle.html#pandas.DataFrame.to_pickle
            df.to_pickle(self.file_path)

    def read(self):
        """
        Sometimes you have to specify the compression level when reading.
            Source: trial and error

        zip = specify or no specify
        gzip = specify
        bz2 = specify or no specify
        zstd = no specify
        xz = no specify
        tar =
        """
        # .read_pickle will detect compression type based on the path given
        #   (but not always compression level)
        #   https://pandas.pydata.org/docs/reference/api/pandas.read_pickle.html#pandas.read_pickle

        if (
            self._compression == "gzip"
            and self._compression_level != None
            and self._compression_level != 0
        ):
            # Dictionary is required if we want to specify compression level
            compression_dict = {
                "method": self._compression,
                self._compression_key: self._compression_level,
            }
            return pd.read_pickle(self.file_path, compression=compression_dict)
        else:
            # .to_pickle will detect compression type based on the path given
            #   https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_pickle.html#pandas.DataFrame.to_pickle
            return pd.read_pickle(self.file_path)
