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

# IO to test
formats = {
    "csv": {
        "write": write_csv,
        "read": lambda path: read_csv_and_convert(path),
        "extension": "csv",
    },
    "csv.gz": {
        "write": write_csv,
        "read": lambda path: read_csv_and_convert(path),
        "extension": "csv.gz",
    },
    # TODO: lots more .csv tests
    # TODO: zip tests
    # TODO: pickle, parquet, feather, hdf tests
    "orc": {
        "write": lambda df, path: df.to_orc(path),
        "read": lambda path: pd.read_orc(path),
        "extension": "orc",
    },
}
