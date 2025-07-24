from formats.AdvancedFormat import AdvancedFormat
import pandas as pd


class CsvFormat(AdvancedFormat):
    """
    Implements reading and writing of Pandas DataFrames in the CSV format
    """

    def __init__(
        self,
        compression: str | None,
        compression_level: int | None,
        read_engine: str | None = None,
    ):
        super().__init__(
            extension="csv", compression=compression, compression_level=compression_level
        )
        # The default read_engine isn't listed documentation. Seems to be 'c' in my tests
        self._read_engine = read_engine

    def __str__(self) -> str:
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
            + self.compression_level_str
            + read_engine_str
        )

    def write(self, df: pd.DataFrame) -> None:
        if self._compression_level:
            # Dictionary is required if we want to specify compression level
            df.to_csv(self.file_path, index=False, compression=self.compression_dict)
        else:
            # .to_csv will detect compression based on the path given
            #   https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html#pandas.DataFrame.to_csv
            df.to_csv(self.file_path, index=False)

    def read(self):
        # .read_csv will detect compression type based on the path given
        #   (but not always compression level)
        #   https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv

        if (
            self._compression == "gzip"
            and self._compression_level != None
            and self._compression_level != 0
        ):
            # Dictionary is required if we want to specify compression level
            if self._read_engine:
                df = pd.read_csv(
                    self.file_path,
                    compression=self.compression_dict,
                    engine=self._read_engine,
                )
            else:
                df = pd.read_csv(self.file_path, compression=self.compression_dict)
        else:
            # .read_csv will detect compression type based on the path given
            #   https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv
            if self._read_engine:
                df = pd.read_csv(self.file_path, engine=self._read_engine)
            else:
                df = pd.read_csv(self.file_path)

        # CSV is just plain text, need to convert object to datetime
        first_column = df.columns[0]
        df[first_column] = pd.to_datetime(df[first_column])
        return df
