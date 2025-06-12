# DataFrame I/O Performance Testing
Testing the speeds and compression of reading and writing DataFrames to/from disk.

## The Situation
You: Have data. You read it, store it, use it. You want to know what is the "best" way to do this.

This repo: Specify your `.csv` file, the repo will load it into a Pandas `DataFrame` then write it and read it through all the many options that Python/Pandas provides. Lastly, it will give you a summary of the performance statistics.

## How to Use
Modify the `input_path` in `read_csv.py`. Then run it: `python3 read_csv.py`. A Dockerfile is provided to manage the repo's requirements.

Example output:
```
Format  DataFrame Memory Difference (B)  Write time to file (s)  Read time from file (s)  Total I/O (s)  Output File Size (kB)  Score (s+MB)  Equivalent DataFrames
11       pickle, gz                                0                0.000288                 0.000224       0.000512                  0.768      0.001280                   True
5         csv, zstd                                0                0.000424                 0.000727       0.001152                  0.295      0.001447                   True
2          csv, bz2                                0                0.000560                 0.000712       0.001272                  0.194      0.001466                   True
12      pickle, bz2                                0                0.000430                 0.000215       0.000645                  0.855      0.001500                   True
[...]
```
