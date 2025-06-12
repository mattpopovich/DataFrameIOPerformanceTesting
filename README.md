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
│ pkl.zip        │ 0          │ 0.041668 │ 0.006924 │ 0.048592 │ 459.323  │ 0.507915 │ True       │
│ pkl.xz         │ 0          │ 0.28461  │ 0.01982  │ 0.30443  │ 361.432  │ 0.665862 │ True       │
│ parquet.brotli │ 0          │ 0.052091 │ 0.00507  │ 0.057161 │ 623.838  │ 0.680999 │ True       │
│ pkl.tar.xz     │ 0          │ 0.288049 │ 0.037372 │ 0.325421 │ 360.44   │ 0.685861 │ True       │
│ parquet.gzip   │ 0          │ 0.049332 │ 0.004689 │ 0.054022 │ 661.682  │ 0.715704 │ True       │
│ pkl.gz         │ 0          │ 0.276763 │ 0.006825 │ 0.283588 │ 463.254  │ 0.746842 │ True       │
│ csv.zip        │ 0          │ 0.229957 │ 0.040773 │ 0.27073  │ 484.679  │ 0.755409 │ True       │
│ pkl.tar.gz     │ 0          │ 0.269622 │ 0.034231 │ 0.303853 │ 463.394  │ 0.767247 │ True       │
│ csv.gz         │ 0          │ 0.314425 │ 0.041021 │ 0.355446 │ 439.988  │ 0.795434 │ True       │
│ csv.tar.gz     │ 0          │ 0.337451 │ 0.048218 │ 0.385669 │ 440.119  │ 0.825788 │ True       │
│ csv.bz2        │ 0          │ 0.416895 │ 0.074304 │ 0.491199 │ 373.99   │ 0.865189 │ True       │
│ csv.tar.bz2    │ 0          │ 0.402397 │ 0.104615 │ 0.507012 │ 374.337  │ 0.881349 │ True       │
│ parquet.zstd   │ 0          │ 0.014657 │ 0.004665 │ 0.019322 │ 868.854  │ 0.888176 │ True       │
│ parquet.snappy │ 0          │ 0.015126 │ 0.00365  │ 0.018776 │ 910.929  │ 0.929705 │ True       │
│ parquet.lz4    │ 0          │ 0.014244 │ 0.003501 │ 0.017745 │ 912.739  │ 0.930484 │ True       │
│ pkl.bz2        │ 0          │ 0.410674 │ 0.037654 │ 0.448328 │ 558.608  │ 1.006936 │ True       │
│ pkl.tar.bz2    │ 0          │ 0.406066 │ 0.074314 │ 0.48038  │ 558.678  │ 1.039058 │ True       │
│ feather        │ 0          │ 0.00897  │ 0.002748 │ 0.011718 │ 1168.73  │ 1.180448 │ True       │
│ parquet        │ 0          │ 0.013602 │ 0.006463 │ 0.020064 │ 1169.968 │ 1.190032 │ True       │
│ csv.tar.xz     │ 0          │ 1.325864 │ 0.073694 │ 1.399558 │ 271.7    │ 1.671258 │ True       │
│ csv.xz         │ 0          │ 1.348208 │ 0.050826 │ 1.399034 │ 272.876  │ 1.67191  │ True       │
│ orc            │ 0          │ 0.018064 │ 0.004655 │ 0.022719 │ 3624.476 │ 3.647195 │ True       │
│ pkl.zstd       │ 0          │ 0.003197 │ 0.002103 │ 0.0053   │ 3729.165 │ 3.734465 │ True       │
│ pkl            │ 0          │ 0.00493  │ 0.0028   │ 0.00773  │ 3729.165 │ 3.736895 │ True       │
│ pkl.tar        │ 0          │ 0.017387 │ 0.002472 │ 0.019859 │ 3737.6   │ 3.757459 │ True       │
│ csv.tar        │ 0          │ 0.205888 │ 0.034736 │ 0.240623 │ 5160.96  │ 5.401583 │ True       │
│ csv.zstd       │ 0          │ 0.229898 │ 0.033934 │ 0.263832 │ 5154.89  │ 5.418722 │ True       │
│ csv            │ 0          │ 0.233829 │ 0.034415 │ 0.268244 │ 5154.89  │ 5.423134 │ True       │
│ h5             │ 709932     │ 0.02253  │ 0.006644 │ 0.029174 │ 5498.248 │ 5.527422 │ True       │
└────────────────┴────────────┴──────────┴──────────┴──────────┴──────────┴──────────┴────────────┘
```
