from abc import ABC, abstractmethod
import pandas as pd
from common import default_file_name, default_folder_name


class BasicFormat(ABC):
    """
    A class that defines what all file formats should implement
    """

    def __init__(
        self,
        extension: str,
        folder_name: str = default_folder_name,
        file_name: str = default_file_name,
    ):
        self._extension = extension
        self._folder_name = folder_name
        self._file_name = file_name

        self.file_path = self._folder_name + "/" + self._file_name + "." + self._extension

    def __str__(self):
        return self._extension

    @abstractmethod
    def write(self, df: pd.DataFrame) -> None:
        """Implement the format-specific writing of the data"""
        raise NotImplementedError

    @abstractmethod
    def read(self):
        """Implement the format-specific reading of the data"""
        raise NotImplementedError
