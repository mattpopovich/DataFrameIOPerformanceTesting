# DataFrame I/O Performance Testing
Testing the speeds and compression of reading and writing DataFrames to/from disk.

## The Situation
You: Have data. You read it, store it, use it. You want to know what is the "best" way to do this.

This repo: Specify your `.csv` file, the repo will load it into a Pandas `DataFrame` then write it and read it through all the many options that Python/Pandas provides. Lastly, it will give you a summary of the performance statistics.

## How to Use
Modify the `input_path` in `read_csv.py`. Then run it: `python3 read_csv.py`. A Dockerfile is provided to manage the repo's requirements.

Example output with a 7.4MB `.csv` file for `input_path`:
```
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
┃                 ┃ DataFrame  ┃          ┃ Read     ┃          ┃ Output   ┃          ┃            ┃
┃                 ┃ Memory     ┃ Write    ┃ time     ┃          ┃ File     ┃          ┃            ┃
┃                 ┃ Difference ┃ time to  ┃ from     ┃ Total    ┃ Size     ┃ Score    ┃ Equivalent ┃
┃ Format          ┃ (B)        ┃ file (s) ┃ file (s) ┃ I/O (s)  ┃ (kB)     ┃ (s+MB)   ┃ DataFrames ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
│ pickle, zip     │ 0          │ 0.040523 │ 0.006965 │ 0.047488 │ 459.315  │ 0.506803 │ True       │
│ pickle, xz      │ 0          │ 0.273472 │ 0.019918 │ 0.29339  │ 361.432  │ 0.654822 │ True       │
│ pickle, tar.xz  │ 0          │ 0.281803 │ 0.038612 │ 0.320415 │ 360.7    │ 0.681115 │ True       │
│ pickle, gz      │ 0          │ 0.262226 │ 0.007226 │ 0.269452 │ 463.25   │ 0.732702 │ True       │
│ pickle, tar.gz  │ 0          │ 0.265351 │ 0.012657 │ 0.278008 │ 463.389  │ 0.741397 │ True       │
│ csv, zip        │ 0          │ 0.237432 │ 0.039729 │ 0.27716  │ 484.671  │ 0.761831 │ True       │
│ csv, gz         │ 0          │ 0.309286 │ 0.039891 │ 0.349177 │ 439.984  │ 0.789161 │ True       │
│ csv, tar.gz     │ 0          │ 0.311353 │ 0.046661 │ 0.358015 │ 440.109  │ 0.798124 │ True       │
│ csv, bz2        │ 0          │ 0.406438 │ 0.071692 │ 0.478131 │ 373.99   │ 0.852121 │ True       │
│ csv, tar.bz2    │ 0          │ 0.407467 │ 0.110038 │ 0.517506 │ 374.482  │ 0.891988 │ True       │
│ pickle, bz2     │ 0          │ 0.393454 │ 0.036282 │ 0.429736 │ 558.608  │ 0.988344 │ True       │
│ pickle, tar.bz2 │ 0          │ 0.389728 │ 0.070767 │ 0.460495 │ 558.83   │ 1.019325 │ True       │
│ feather         │ 0          │ 0.008165 │ 0.002642 │ 0.010807 │ 1168.73  │ 1.179537 │ True       │
│ csv, xz         │ 0          │ 1.270863 │ 0.050029 │ 1.320891 │ 272.876  │ 1.593767 │ True       │
│ csv, tar.xz     │ 0          │ 1.270053 │ 0.068833 │ 1.338886 │ 271.764  │ 1.61065  │ True       │
│ orc             │ 0          │ 0.017623 │ 0.004903 │ 0.022526 │ 3624.476 │ 3.647002 │ True       │
│ pickle, zstd    │ 0          │ 0.003065 │ 0.001921 │ 0.004986 │ 3729.165 │ 3.734151 │ True       │
│ pickle          │ 0          │ 0.003089 │ 0.002786 │ 0.005875 │ 3729.165 │ 3.73504  │ True       │
│ pickle, tar     │ 0          │ 0.018503 │ 0.002514 │ 0.021017 │ 3737.6   │ 3.758617 │ True       │
│ csv, tar        │ 0          │ 0.197797 │ 0.033551 │ 0.231348 │ 5160.96  │ 5.392308 │ True       │
│ csv, zstd       │ 0          │ 0.220133 │ 0.033987 │ 0.254119 │ 5154.89  │ 5.409009 │ True       │
│ csv             │ 0          │ 0.22126  │ 0.033902 │ 0.255162 │ 5154.89  │ 5.410052 │ True       │
│ hdf             │ 709932     │ 0.022126 │ 0.006193 │ 0.028319 │ 5498.248 │ 5.526567 │ True       │
└─────────────────┴────────────┴──────────┴──────────┴──────────┴──────────┴──────────┴────────────┘
```
