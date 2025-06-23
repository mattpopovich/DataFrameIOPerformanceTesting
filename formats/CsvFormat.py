from formats.BasicFormat import BasicFormat
import pandas as pd


# TODO: Lots of copypasta between this and PickleFormat.py. Maybe make a new class?
class CsvFormat(BasicFormat):
    """
    Implements reading and writing of Pandas DataFrames in the CSV format
    """

    def __init__(
        self,
        compression: str | None,
        compression_level: int | None,
        read_engine: str | None = None,
    ):
        super().__init__(extension="csv")
        if compression_level != None:
            self.file_path = f"{self._folder_name}/{self._file_name}C{compression_level}.{self._extension}"
        self._compression = compression
        # The compression type is zstd but the file extension is zst
        self._compression_extension = "zst" if compression == "zstd" else compression
        self._compression_level = compression_level
        self._read_engine = read_engine  # TODO: What is the default read_engine? Not listed in documentation. Seems to be 'c' in my tests

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
        if self._read_engine == "c":
            read_engine_str = " Rc"
        elif self._read_engine == "python":
            read_engine_str = " Rpy"
        elif self._read_engine == "pyarrow":
            read_engine_str = " Rpy→"
        else:
            read_engine_str = ""

        return (
            self._extension
            + self._compression_path
            + compression_level_str
            + read_engine_str
        )

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
            df.to_csv(self.file_path, index=False, compression=compression_dict)
        else:
            # .to_csv will detect compression based on the path given
            #   https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html#pandas.DataFrame.to_csv
            df.to_csv(self.file_path, index=False)

    def read(self):
        """
        Sometimes you have to specify the compression level when reading.
            Source: trial and error from PickleFormat.read()

        zip = specify or no specify
        gzip = specify
        bz2 = specify or no specify
        zstd = no specify
        xz = no specify
        tar =
        """

        # .read_csv will detect compression type based on the path given
        #   (but not always compression level)
        #   https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv

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
            if self._read_engine:
                df = pd.read_csv(
                    self.file_path, compression=compression_dict, engine=self._read_engine
                )
            else:
                df = pd.read_csv(self.file_path, compression=compression_dict)
        else:
            # .read_csv will detect compression type based on the path given
            #   https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv
            if self._read_engine:
                df = pd.read_csv(self.file_path, engine=self._read_engine)
            else:
                df = pd.read_csv(self.file_path)

        first_column = df.columns[0]
        df[first_column] = pd.to_datetime(df[first_column])
        return df
