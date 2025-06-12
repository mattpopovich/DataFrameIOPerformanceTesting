"""
Collection of formats that `read_csv.py` will I/O test
"""

import pandas as pd


# IO to test
#       See https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_pickle.html
# "parquet": {
#     "write": lambda df, output_path, engine, compression: df.to_parquet(
#         output_path, engine=engine, compression=compression
#     ),
#     "compressions": [None, "snappy", "gzip", "brotli", "lz4", "zstd"],
#     "engines": ["pyarrow", "fastparquet"],
#     "read": lambda path: pd.read_parquet(path),
#     "extension": "parquet",
# },
