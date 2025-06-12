from BasicFormat import BasicFormat
import pandas as pd


class ParquetFormat(BasicFormat):
    """
    Implements reading and writing of Pandas DataFrames in the Parquet format
    """

    def __init__(self, compression: str | None):
        super().__init__(extension="parquet")
        self._compression = compression

        # Add compression to file path (if necessary)
        self._compression_path = "." + self._compression if self._compression else ""
        self.file_path += self._compression_path

    def __str__(self):
        return self._extension + self._compression_path

    def write(self, df: pd.DataFrame) -> None:
        # TODO: Specify engines["pyarrow", "fastparquet"]
        df.to_parquet(self.file_path, compression=self._compression, index=False)

    def read(self):
        # TODO: Specify engines ["pyarrow", "fastparquet"]
        return pd.read_parquet(self.file_path)
