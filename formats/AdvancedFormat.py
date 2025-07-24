import pandas as pd

from formats.BasicFormat import BasicFormat


class AdvancedFormat(BasicFormat):
    """
    A class that defines what advanced formats should implement.
    These formats will have compression + read/write engines which adds complexity
    """

    def __init__(
        self, extension: str, compression: str | None, compression_level: int | None
    ):
        super().__init__(extension=extension)
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

        self.compression_level_str = (
            " C=" + str(self._compression_level)
            if self._compression_level != None
            else ""
        )

        self.compression_dict = {
            "method": self._compression,
            self._compression_key: self._compression_level,
        }

    def __str__(self) -> str:
        raise NotImplementedError

    def write(self, df: pd.DataFrame) -> None:
        """
        zip = compresslevel: 0 - 9 : https://docs.python.org/3/library/gzip.html
        gzip = compresslevel: -1 - 9
        bz2 = compresslevel: 1 - 9
        zstd = level: -7 - 22
        xz = preset: 0 - 9
        """
        raise NotImplementedError

    def read(self):
        """
        Sometimes you have to specify the compression level when reading.
            Source: trial and error

        zip = specify or no specify
        gzip = specify
        bz2 = specify or no specify
        zstd = no specify
        xz = no specify
        """
        raise NotImplementedError
