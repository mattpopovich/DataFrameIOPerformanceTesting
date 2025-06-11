import pandas as pd
import os
import time


# File paths
input_path = "data_big.csv"
output_path = "output.csv"


def read_csv_and_convert(path):
    df = pd.read_csv(path)
    first_column = df.columns[0]
    df[first_column] = pd.to_datetime(df[first_column])
    return df


# IO to test
formats = {
    "csv": {
        "write": lambda df: df.to_csv(
            output_path,
            index=False,
            float_format="%.8f",
            date_format="%Y-%m-%dT%H:%M:%S.%f",
        ),
        "read": lambda path: read_csv_and_convert(path),
        "extension": "csv",
    }
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

    ### Write tests
    start_time_s = time.perf_counter()
    operation["write"](df)
    end_time_s = time.perf_counter()
    write_time_s = end_time_s - start_time_s

    output_file_size_B = os.path.getsize(output_path)

    #### Make sure written file matches
    with open("data.csv", "rb") as f1, open(output_path, "rb") as f2:
        if f1.read() == f2.read():
            print(f"'{output_path}' matched.")
        else:
            print(f"'{output_path}' does not match '{input_path}'.")

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
            "Write time to file": write_time_s,
            "Read time from file": read_time_s,
            "Output File Size (kB)": output_file_size_B / 1000,
            "Equivalent DataFrames": df.equals(df2),
        }
    )

results_df = pd.DataFrame(results)
print(results_df)
