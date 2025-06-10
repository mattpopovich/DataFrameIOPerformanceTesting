import pandas as pd
import os


# File paths
input_path = "data.csv"
output_path = "output.csv"

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

### Write tests
df.to_csv(
    output_path, index=False, float_format="%.8f", date_format="%Y-%m-%dT%H:%M:%S.%f"
)

#### Make sure written file matches
with open("data.csv", "rb") as f1, open(output_path, "rb") as f2:
    if f1.read() == f2.read():
        print(f"'{output_path}' matched.")
    else:
        print(f"'{output_path}' does not match '{input_path}'.")

#### Make sure we can read back into a DataFrame
df2 = pd.read_csv(output_path)
df2[first_column] = pd.to_datetime(df[first_column])

if df.equals(df2):
    print(f"DataFrame created from {output_path} is an exact match")
    os.remove(output_path)
else:
    print(
        f"ERROR: DataFrame created from {output_path} does not match the original dataframe"
    )
