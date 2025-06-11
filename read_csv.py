import pandas as pd
import os
import time


# File paths
input_path = "data.csv"
output_name = "output"


def read_csv_and_convert(path):
    df = pd.read_csv(path)
    first_column = df.columns[0]
    df[first_column] = pd.to_datetime(df[first_column])
    return df


write_csv = lambda df, output_path: df.to_csv(
    output_path,
    index=False,
    float_format="%.8f",
    date_format="%Y-%m-%dT%H:%M:%S.%f",
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
}

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

    # Only non-compressed .csv file should match
    with open(input_path, "rb") as f1, open(output_path, "rb") as f2:
        csv_files_equal = f1.read() == f2.read()

    #### Make sure we can read back into a DataFrame
    start_time_s = time.perf_counter()
    df2 = operation["read"](output_path)
    end_time_s = time.perf_counter()
    read_time_s = end_time_s - start_time_s

    if df.equals(df2):
        print(f"DataFrame created from {output_path} is an exact match")
        os.remove(output_path)
    else:
        print(
            f"ERROR: DataFrame created from {output_path} does not match the original dataframe"
        )

    results.append(
        {
            "Format": format,
            "Original DataFrame Memory (kB)": df.memory_usage().sum() / 1000,
            "Write time to file (s)": write_time_s,
            "Read time from file (s)": read_time_s,
            "Total I/O (s)": write_time_s + read_time_s,
            "Output File Size (kB)": output_file_size_B / 1000,
            "Final DataFrame Memory (kB)": df2.memory_usage().sum() / 1000,
            "Equivalent DataFrames": df.equals(df2),
            "Equivalent .csv files": csv_files_equal,
        }
    )

results_df = pd.DataFrame(results)
print(results_df)
