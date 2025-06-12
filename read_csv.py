import pandas as pd
import os
import time

from textwrap import wrap
from tabulate import tabulate

from formats_to_test import formats
from pretty_print_dataframe import pretty_print_dataframe

## TODO: Save temp files in a directory

# File paths
input_path = "data.csv"  # CHANGE THIS to get performance numbers for your file
output_name = "output"
score_header_name = "Score (s+MB)"


results: list[dict] = []

df = pd.read_csv(input_path)

print(f"DataFrame initially read into memory:")
df.info()
print()

### Convert dataframe into correct datatypes here ###
first_column = df.columns[0]
df[first_column] = pd.to_datetime(df[first_column])
#####################################################
print(f"DataFrame after converting to correct data types:")
df.info()
print()

for format, operation in formats.items():
    print(f"analyzing format {format}")

    if "compressions" in operation:
        compressions = operation["compressions"]
    else:
        compressions = [False]

    output_path = output_name + "." + operation["extension"]
    full_format = format

    for compression in compressions:
        print(f"analyzing compression {compression}")

        if compression:
            output_path = output_name + "." + compression
            full_format = format + ", " + compression

        ### Write tests
        start_time_s = time.perf_counter()
        if compression == False:
            operation["write"](df, output_path)
        else:
            if compression == None:
                compression_dict = None
            else:
                compression_dict = {"method": compression}

            operation["write"](df, output_path)
        end_time_s = time.perf_counter()
        write_time_s = end_time_s - start_time_s

        print(f"wrote output path {output_path}")
        output_file_size_B = os.path.getsize(output_path)

        #### Make sure we can read back into a DataFrame
        start_time_s = time.perf_counter()
        df2 = operation["read"](output_path)
        end_time_s = time.perf_counter()
        read_time_s = end_time_s - start_time_s

        dataframe_memory_difference_B = (
            df2.memory_usage().sum() - df.memory_usage().sum()
        )
        total_io_s = write_time_s + read_time_s
        results.append(
            {
                "Format": full_format,
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
pretty_print_dataframe(results_df)
