from BasicFormat import BasicFormat
import pandas as pd


class FeatherFormat(BasicFormat):
    """
    Implements reading and writing of Pandas DataFrames in the Feather format
    """

    def __init__(self):
        super().__init__(extension="feather")

    def write(self, df: pd.DataFrame) -> None:
        df.to_feather(self.file_path)

    def read(self):
        return pd.read_feather(self.file_path)
