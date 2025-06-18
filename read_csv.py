import pandas as pd
import os
import time
import argparse

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

# Constants
input_path = "data.csv"  # CHANGE THIS to get performance numbers for your file

# DataFrame keys (_t ~ titles)
score_t = "Score (lower is better)"
total_io_normalized_t = "Total I/O Normalized"
output_file_size_orig_t = "Output File Size (% Orig.)"
output_file_size_norm_t = "Output File Size Normalized"
total_io_t = "Total I/O (s)"

parser = argparse.ArgumentParser()
parser.add_argument(
    "-v",
    "--verbose",
    help="Run with all possible compression levels",
    action="store_true",
)
parser.add_argument(
    "-k", "--keep", help="Keep all generated output files", action="store_true"
)
args = parser.parse_args()

results: list[dict] = []
formats: list[BasicFormat] = []

# Create the formats that we want to test
formats.extend(CsvFormat(compression) for compression in list_of_compressions)
formats.extend(
    PickleFormat(compression, compression_level)
    for compression in ["zip", "xz"]
    for compression_level in (list(range(0, 10)) + [None] if args.verbose else [None])
)
formats.extend(
    PickleFormat(compression, compression_level)
    for compression in ["gzip"]
    for compression_level in (list(range(-1, 10)) + [None] if args.verbose else [None])
)  # Not sure why -1 works but we'll include it
formats.extend(
    PickleFormat(compression, compression_level)
    for compression in ["bz2"]
    for compression_level in (list(range(1, 10)) + [None] if args.verbose else [None])
)
formats.extend(
    PickleFormat(compression, compression_level)
    for compression in ["zstd"]
    for compression_level in (list(range(-7, 23)) + [None] if args.verbose else [None])
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
input_file_size_B = os.path.getsize(input_path)

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
            total_io_t: total_io_s,
            output_file_size_orig_t: output_file_size_B / input_file_size_B * 100,
            "Equivalent DataFrames": df.equals(df2),
        }
    )

    if not args.keep:
        os.remove(format.file_path)

results_df = pd.DataFrame(results)

# Define your desired score here
results_df[total_io_normalized_t] = results_df[total_io_t] / min(results_df[total_io_t])
results_df[output_file_size_norm_t] = results_df[output_file_size_orig_t] / min(
    results_df[output_file_size_orig_t]
)
results_df[score_t] = (
    results_df[total_io_normalized_t] + results_df[output_file_size_norm_t]
)

results_df = results_df.sort_values(score_t)  # Lower score is better
# results_df = results_df.sort_values("Output File Size (kB)")  # Identify bad compressions
pretty_print_dataframe(results_df)
