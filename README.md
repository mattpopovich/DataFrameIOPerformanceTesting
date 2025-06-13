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
│ pkl.zst        │ 0          │ 0.006738 │ 0.003112 │ 0.00985  │ 462.505  │ 0.472355 │ True       │
│ pkl.zip        │ 0          │ 0.041707 │ 0.007614 │ 0.049321 │ 459.323  │ 0.508644 │ True       │
│ parquet.brotli │ 0          │ 0.046727 │ 0.004155 │ 0.050882 │ 623.838  │ 0.67472  │ True       │
│ pkl.xz         │ 0          │ 0.303685 │ 0.021044 │ 0.324729 │ 361.432  │ 0.686161 │ True       │
│ parquet.gzip   │ 0          │ 0.045335 │ 0.004425 │ 0.04976  │ 661.682  │ 0.711442 │ True       │
│ csv.zst        │ 0          │ 0.174624 │ 0.034306 │ 0.20893  │ 509.054  │ 0.717984 │ True       │
│ csv.zip        │ 0          │ 0.205823 │ 0.040128 │ 0.245951 │ 484.679  │ 0.73063  │ True       │
│ pkl.gz         │ 0          │ 0.264047 │ 0.007393 │ 0.27144  │ 463.254  │ 0.734694 │ True       │
│ csv.gz         │ 0          │ 0.301187 │ 0.040413 │ 0.3416   │ 439.988  │ 0.781588 │ True       │
│ csv.bz2        │ 0          │ 0.383741 │ 0.068503 │ 0.452244 │ 373.99   │ 0.826234 │ True       │
│ parquet.zstd   │ 0          │ 0.012687 │ 0.002829 │ 0.015515 │ 868.854  │ 0.884369 │ True       │
│ parquet.snappy │ 0          │ 0.012762 │ 0.003418 │ 0.016181 │ 910.929  │ 0.92711  │ True       │
│ parquet.lz4    │ 0          │ 0.012862 │ 0.002737 │ 0.015599 │ 912.739  │ 0.928338 │ True       │
│ pkl.bz2        │ 0          │ 0.408111 │ 0.038779 │ 0.44689  │ 558.608  │ 1.005498 │ True       │
│ feather        │ 0          │ 0.008674 │ 0.002553 │ 0.011228 │ 1168.73  │ 1.179958 │ True       │
│ parquet        │ 0          │ 0.01621  │ 0.006089 │ 0.0223   │ 1169.968 │ 1.192268 │ True       │
│ csv.xz         │ 0          │ 1.302666 │ 0.04942  │ 1.352086 │ 272.876  │ 1.624962 │ True       │
│ orc            │ 0          │ 0.018786 │ 0.004359 │ 0.023145 │ 3624.476 │ 3.647621 │ True       │
│ pkl            │ 0          │ 0.003475 │ 0.003183 │ 0.006658 │ 3729.165 │ 3.735823 │ True       │
│ csv            │ 0          │ 0.215998 │ 0.034679 │ 0.250677 │ 5154.89  │ 5.405567 │ True       │
│ h5             │ 709932     │ 0.023344 │ 0.008735 │ 0.032079 │ 5498.248 │ 5.530327 │ True       │
└────────────────┴────────────┴──────────┴──────────┴──────────┴──────────┴──────────┴────────────┘
```
