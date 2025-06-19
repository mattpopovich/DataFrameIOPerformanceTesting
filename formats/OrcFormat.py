from formats.BasicFormat import BasicFormat
import pandas as pd


class OrcFormat(BasicFormat):
    """
    Implements reading and writing of Pandas DataFrames in the Orc format
    """

    def __init__(self):
        super().__init__(extension="orc")

    def write(self, df: pd.DataFrame) -> None:
        df.to_orc(self.file_path)

    def read(self):
        return pd.read_orc(self.file_path)
