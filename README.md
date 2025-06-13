# DataFrame I/O Performance Testing
Testing the speeds and compression of reading and writing DataFrames to/from disk.

## The Situation
You: Have data. You read it, store it, use it. You want to know what is the "best" way to do this.

This repo: Specify your `.csv` file, the repo will load it into a Pandas `DataFrame` then write it and read it through all the many options that Python/Pandas provides. Lastly, it will give you a summary of the performance statistics.

## How to Use
Modify the `input_path` in `read_csv.py`. Then run it: `python3 read_csv.py`. A Dockerfile is provided to manage the repo's requirements.

Example output with a 7.4MB `.csv` file for `input_path`:
```
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
┃                ┃ DataFrame  ┃          ┃ Read     ┃          ┃ Output   ┃          ┃            ┃
┃                ┃ Memory     ┃ Write    ┃ time     ┃          ┃ File     ┃          ┃            ┃
┃                ┃ Difference ┃ time to  ┃ from     ┃ Total    ┃ Size     ┃ Score    ┃ Equivalent ┃
┃ Format         ┃ (B)        ┃ file (s) ┃ file (s) ┃ I/O (s)  ┃ (kB)     ┃ (s+MB)   ┃ DataFrames ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
│ pkl.zip        │ 0          │ 0.040981 │ 0.007099 │ 0.048081 │ 459.323  │ 0.507404 │ True       │
│ pkl.xz         │ 0          │ 0.279874 │ 0.020557 │ 0.300431 │ 361.432  │ 0.661863 │ True       │
│ parquet.brotli │ 0          │ 0.05207  │ 0.004215 │ 0.056285 │ 623.838  │ 0.680123 │ True       │
│ parquet.gzip   │ 0          │ 0.045637 │ 0.004692 │ 0.05033  │ 661.682  │ 0.712012 │ True       │
│ pkl.gz         │ 0          │ 0.263405 │ 0.007063 │ 0.270468 │ 463.254  │ 0.733722 │ True       │
│ csv.zip        │ 0          │ 0.217789 │ 0.040804 │ 0.258593 │ 484.679  │ 0.743272 │ True       │
│ csv.gz         │ 0          │ 0.313123 │ 0.040336 │ 0.353459 │ 439.988  │ 0.793447 │ True       │
│ csv.bz2        │ 0          │ 0.398703 │ 0.073919 │ 0.472622 │ 373.99   │ 0.846612 │ True       │
│ parquet.zstd   │ 0          │ 0.01303  │ 0.002972 │ 0.016002 │ 868.854  │ 0.884856 │ True       │
│ parquet.snappy │ 0          │ 0.013401 │ 0.003115 │ 0.016516 │ 910.929  │ 0.927445 │ True       │
│ parquet.lz4    │ 0          │ 0.013041 │ 0.002864 │ 0.015905 │ 912.739  │ 0.928644 │ True       │
│ pkl.bz2        │ 0          │ 0.384507 │ 0.037152 │ 0.421659 │ 558.608  │ 0.980267 │ True       │
│ feather        │ 0          │ 0.008371 │ 0.002559 │ 0.01093  │ 1168.73  │ 1.17966  │ True       │
│ parquet        │ 0          │ 0.015035 │ 0.005834 │ 0.020869 │ 1169.968 │ 1.190837 │ True       │
│ csv.xz         │ 0          │ 1.290335 │ 0.050415 │ 1.34075  │ 272.876  │ 1.613626 │ True       │
│ orc            │ 0          │ 0.017704 │ 0.004453 │ 0.022157 │ 3624.476 │ 3.646633 │ True       │
│ pkl.zstd       │ 0          │ 0.003367 │ 0.001948 │ 0.005315 │ 3729.165 │ 3.73448  │ True       │
│ pkl            │ 0          │ 0.003648 │ 0.002919 │ 0.006567 │ 3729.165 │ 3.735732 │ True       │
│ csv            │ 0          │ 0.225131 │ 0.033482 │ 0.258612 │ 5154.89  │ 5.413502 │ True       │
│ csv.zstd       │ 0          │ 0.228438 │ 0.048263 │ 0.276702 │ 5154.89  │ 5.431592 │ True       │
│ h5             │ 709932     │ 0.022672 │ 0.007928 │ 0.0306   │ 5498.248 │ 5.528848 │ True       │
└────────────────┴────────────┴──────────┴──────────┴──────────┴──────────┴──────────┴────────────┘
```
