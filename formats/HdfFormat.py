from formats.BasicFormat import BasicFormat
import pandas as pd


class HdfFormat(BasicFormat):
    """
    Implements reading and writing of Pandas DataFrames in the HDF (.hdf5, .h5) format
    """

    def __init__(self):
        super().__init__(extension="h5")

    def write(self, df: pd.DataFrame) -> None:
        df.to_hdf(self.file_path, key="data", mode="w")

    def read(self):
        return pd.read_hdf(self.file_path)
