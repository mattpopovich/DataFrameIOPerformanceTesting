import pandas as pd
import os
import time
import argparse

from tqdm import tqdm

from pretty_print_dataframe import pretty_print_dataframe

from formats.BasicFormat import BasicFormat
from formats.CsvFormat import CsvFormat
from formats.FeatherFormat import FeatherFormat
from formats.HdfFormat import HdfFormat
from formats.OrcFormat import OrcFormat
from formats.ParquetFormat import ParquetFormat

from common import get_pickle_formats
from config import list_of_compressions, default_folder_name


# DataFrame keys (_t ~ titles)
score_t = "Score (lower is better)"
total_io_normalized_t = "Total I/O Normalized"
output_file_size_orig_t = "Output File Size (% Orig.)"
output_file_size_norm_t = "Output File Size Normalized"
total_io_t = "Total I/O (s)"
dataframe_memory_difference_t = "DataFrame Memory Difference (B)"
equivalent_dataframes_t = "Equivalent DataFrames"

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f", "--file", help="Specify the file that should be used for analysis"
)
parser.add_argument(
    "-k", "--keep", help="Keep all generated output files", action="store_true"
)
parser.add_argument(
    "-v",
    "--verbose",
    help="Run with all possible compression levels and show some additional columns",
    action="store_true",
)
args = parser.parse_args()

results: list[dict] = []
formats: list[BasicFormat] = []
input_path: str = "data.csv" if not args.file else args.file  # Default if no arg passed

# Create the formats that we want to test
formats.extend(CsvFormat(compression) for compression in list_of_compressions)
formats.extend(get_pickle_formats(args.verbose))
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

print(f"DataFrame initially read into memory from {input_path}:")
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

    # Write tests
    start_time_s = time.perf_counter()
    format.write(df)
    end_time_s = time.perf_counter()
    write_time_s = end_time_s - start_time_s

    # print(f"wrote output path {format.file_path}")
    output_file_size_B = os.path.getsize(format.file_path)

    # Make sure we can read back into a DataFrame
    start_time_s = time.perf_counter()
    df2 = format.read()
    end_time_s = time.perf_counter()
    read_time_s = end_time_s - start_time_s

    dataframe_memory_difference_B = df2.memory_usage().sum() - df.memory_usage().sum()
    total_io_s = write_time_s + read_time_s
    results.append(
        {
            "Format": format,
            dataframe_memory_difference_t: dataframe_memory_difference_B,
            "Write time to file (s)": write_time_s,
            "Read time from file (s)": read_time_s,
            total_io_t: total_io_s,
            output_file_size_orig_t: output_file_size_B / input_file_size_B * 100,
            equivalent_dataframes_t: df.equals(df2),
        }
    )

    if not args.keep:
        os.remove(format.file_path)

results_df = pd.DataFrame(results)

# Define the desired score here
results_df[total_io_normalized_t] = results_df[total_io_t] / min(results_df[total_io_t])
results_df[output_file_size_norm_t] = results_df[output_file_size_orig_t] / min(
    results_df[output_file_size_orig_t]
)
results_df[score_t] = (
    results_df[total_io_normalized_t] + results_df[output_file_size_norm_t]
)

results_df = results_df.sort_values(score_t)  # Lower score is better
# results_df = results_df.sort_values("Output File Size (kB)")  # Identify bad compressions

# Remove unnecessary columns
if not args.verbose:
    results_df.drop(
        columns=[dataframe_memory_difference_t, equivalent_dataframes_t], inplace=True
    )
pretty_print_dataframe(results_df)
