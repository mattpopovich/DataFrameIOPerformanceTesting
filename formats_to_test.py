"""
Collection of formats that `read_csv.py` will I/O test
"""

import pandas as pd


def read_csv_and_convert(path):
    df = pd.read_csv(path)
    first_column = df.columns[0]
    df[first_column] = pd.to_datetime(df[first_column])
    return df


write_csv = lambda df, output_path: df.to_csv(
    output_path,
    index=False,
)

# Given in https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_pickle.html
list_of_compressions = [
    None,
    "gz",
    "bz2",
    "zip",
    "xz",
    "zstd",
    "tar",
    "tar.gz",
    "tar.xz",
    "tar.bz2",
]

# IO to test
formats = {
    "csv": {
        "write": write_csv,
        "compressions": list_of_compressions,
        "read": lambda path: read_csv_and_convert(path),
        "extension": "csv",
    },
    # TODO: zip tests
    # TODO: parquet tests
    "pickle": {
        "write": lambda df, output_path: df.to_pickle(output_path),
        "compressions": list_of_compressions,
        "read": lambda path: pd.read_pickle(path),
        "extension": "pkl",
    },
    "feather": {
        "write": lambda df, output_path: df.to_feather(output_path),
        "read": lambda path: pd.read_feather(path),
        "extension": "feather",
    },
    "hdf": {
        "write": lambda df, output_path: df.to_hdf(output_path, key="data", mode="w"),
        "read": lambda path: pd.read_hdf(path),
        "extension": "h5",
    },
    "orc": {
        "write": lambda df, output_path: df.to_orc(output_path),
        "read": lambda path: pd.read_orc(path),
        "extension": "orc",
    },
}
