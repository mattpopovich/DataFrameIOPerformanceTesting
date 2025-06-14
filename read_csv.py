import pandas as pd
import os
import time

from textwrap import wrap
from tabulate import tabulate
from tqdm import tqdm

from pretty_print_dataframe import pretty_print_dataframe

from BasicFormat import BasicFormat
from CsvFormat import CsvFormat
from FeatherFormat import FeatherFormat
from HdfFormat import HdfFormat
from OrcFormat import OrcFormat
from PickleFormat import PickleFormat
from ParquetFormat import ParquetFormat

from common import list_of_compressions, default_folder_name

# TODO: flag to specify their own csv file
# TODO: flag to not save output files
# TODO: Flag to not run all the permutations of compressions

# Constants
input_path = "data.csv"  # CHANGE THIS to get performance numbers for your file
score_header_name = "Score (s+MB)"


results: list[dict] = []
formats: list[BasicFormat] = []

# Create the formats that we want to test
formats.extend(CsvFormat(compression) for compression in list_of_compressions)
formats.extend(
    PickleFormat(compression, compression_level)
    for compression in ["zip", "xz"]
    for compression_level in list(range(0, 10)) + [None]
)
formats.extend(
    PickleFormat(compression, compression_level)
    for compression in ["gzip"]
    for compression_level in list(range(-1, 10)) + [None]
)  # Not sure why -1 works but we'll include it
formats.extend(
    PickleFormat(compression, compression_level)
    for compression in ["bz2"]
    for compression_level in list(range(1, 10)) + [None]
)
formats.extend(
    PickleFormat(compression, compression_level)
    for compression in ["zstd"]
    for compression_level in list(range(-7, 23)) + [None]
)
formats.append(PickleFormat(None, None))
formats.append(FeatherFormat())
formats.append(HdfFormat())
formats.append(OrcFormat())
formats.extend(
    ParquetFormat(compression)
    for compression in [None, "snappy", "gzip", "brotli", "lz4", "zstd"]
)

os.makedirs(default_folder_name, exist_ok=True)
df = pd.read_csv(input_path)

print(f"DataFrame initially read into memory:")
df.info()
print()

# Convert dataframe into correct datatypes here
first_column = df.columns[0]
df[first_column] = pd.to_datetime(df[first_column])
print(f"DataFrame after converting to correct data types:")
df.info()
print()

for format in tqdm(formats):

    # print(f"analyzing format {format}")

    ### Write tests
    start_time_s = time.perf_counter()
    format.write(df)
    end_time_s = time.perf_counter()
    write_time_s = end_time_s - start_time_s

    # print(f"wrote output path {format.file_path}")
    output_file_size_B = os.path.getsize(format.file_path)

    #### Make sure we can read back into a DataFrame
    start_time_s = time.perf_counter()
    df2 = format.read()
    end_time_s = time.perf_counter()
    read_time_s = end_time_s - start_time_s

    dataframe_memory_difference_B = df2.memory_usage().sum() - df.memory_usage().sum()
    total_io_s = write_time_s + read_time_s
    results.append(
        {
            "Format": format,
            "DataFrame Memory Difference (B)": dataframe_memory_difference_B,
            "Write time to file (s)": write_time_s,
            "Read time from file (s)": read_time_s,
            "Total I/O (s)": total_io_s,
            "Output File Size (kB)": output_file_size_B / 1e3,
            score_header_name: total_io_s + output_file_size_B / 1e6,
            "Equivalent DataFrames": df.equals(df2),
        }
    )

results_df = pd.DataFrame(results)
results_df = results_df.sort_values(score_header_name)  # Lower score is better
# results_df = results_df.sort_values("Output File Size (kB)")  # Identify bad compressions
pretty_print_dataframe(results_df)
