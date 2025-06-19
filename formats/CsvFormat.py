from formats.BasicFormat import BasicFormat
import pandas as pd


class CsvFormat(BasicFormat):
    """
    Implements reading and writing of Pandas DataFrames in the CSV format
    """

    def __init__(self, compression: str | None):
        super().__init__(extension="csv")
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

        # .to_csv will detect compression based on the path given
        #   https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html#pandas.DataFrame.to_csv
        df.to_csv(self.file_path, index=False)

    def read(self):
        # TODO: Specify the engine

        # .read_csv will detect compression based on the path given
        #   https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv
        df = pd.read_csv(self.file_path)
        first_column = df.columns[0]
        df[first_column] = pd.to_datetime(df[first_column])
        return df
