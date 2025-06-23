from formats.BasicFormat import BasicFormat
import pandas as pd


class ParquetFormat(BasicFormat):
    """
    Implements reading and writing of Pandas DataFrames in the Parquet format
    """

    def __init__(self, compression: str | None, engine: str = "auto"):
        super().__init__(extension="parquet")
        self._compression = compression
        self._engine = engine

        # Add compression to file path (if necessary)
        self._compression_path = ("." + self._compression) if self._compression else ""
        self.file_path = (
            self._folder_name
            + "/"
            + self._file_name
            + "-"
            + self._engine
            + "."
            + self._extension
            + self._compression_path
        )

    def __str__(self):
        if self._engine == "auto":
            engine_str = ""
        elif self._engine == "pyarrow":
            engine_str = "py→"
        elif self._engine == "fastparquet":
            engine_str = "fastP"
        else:
            engine_str = self._engine

        return self._extension + self._compression_path + " " + engine_str

    def write(self, df: pd.DataFrame) -> None:
        # https://stackoverflow.com/a/77105313/4368898
        df.to_parquet(
            self.file_path,
            engine=self._engine,
            compression=self._compression,
            index=False,
        )

    def read(self):
        # TODO: Specify engines ["pyarrow", "fastparquet"]
        return pd.read_parquet(self.file_path)
