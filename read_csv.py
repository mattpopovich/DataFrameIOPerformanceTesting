import pandas as pd
import os
import time

from formats_to_test import formats

# File paths
input_path = "data.csv"
output_name = "output"


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
    output_path = output_name + "." + operation["extension"]

    ### Write tests
    start_time_s = time.perf_counter()
    operation["write"](df, output_path)
    end_time_s = time.perf_counter()
    write_time_s = end_time_s - start_time_s

    output_file_size_B = os.path.getsize(output_path)

    #### Make sure we can read back into a DataFrame
    start_time_s = time.perf_counter()
    df2 = operation["read"](output_path)
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
            "Score (s*kB)": total_io_s * output_file_size_B / 1e3,
            "Equivalent DataFrames": df.equals(df2),
        }
    )

results_df = pd.DataFrame(results)
print(results_df.sort_values("Score (s*kB)"))  # Lower score is better
