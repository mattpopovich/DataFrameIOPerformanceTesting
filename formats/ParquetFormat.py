from formats.BasicFormat import BasicFormat
import pandas as pd


class ParquetFormat(BasicFormat):
    """
    Implements reading and writing of Pandas DataFrames in the Parquet format
    """

    def __init__(
        self,
        compression: str | None,
        write_engine: str = "auto",
        read_engine: str = "auto",
    ):
        super().__init__(extension="parquet")
        self._compression = compression
        self._write_engine = write_engine
        self._read_engine = read_engine

        # Add compression to file path (if necessary)
        self._compression_path = ("." + self._compression) if self._compression else ""
        self.file_path = (
            self._folder_name
            + "/"
            + self._file_name
            + "-"
            + self._write_engine
            + "."
            + self._extension
            + self._compression_path
        )

    def __str__(self):
        if self._write_engine == "auto":
            write_engine_str = ""
        elif self._write_engine == "pyarrow":
            write_engine_str = " Wpy→"
        elif self._write_engine == "fastparquet":
            write_engine_str = " WfastP"
        else:
            write_engine_str = self._write_engine

        if self._read_engine == "auto":
            read_engine_str = ""
        elif self._read_engine == "pyarrow":
            read_engine_str = " Rpy→"
        elif self._read_engine == "fastparquet":
            read_engine_str = " RfastP"
        else:
            read_engine_str = self._read_engine

        return (
            self._extension + self._compression_path + write_engine_str + read_engine_str
        )

    def write(self, df: pd.DataFrame) -> None:
        # https://stackoverflow.com/a/77105313/4368898
        df.to_parquet(
            self.file_path,
            engine=self._write_engine,
            compression=self._compression,
            index=False,
        )

    def read(self):
        return pd.read_parquet(self.file_path, engine=self._read_engine)
