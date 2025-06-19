# Given in https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_pickle.html
list_of_compressions = [
    None,
    "gz",
    "bz2",
    "zip",
    "xz",
    "zstd",
    # "tar",        # .tar just combines things into one file. No compression
    # "tar.gz",     # Same as .gz
    # "tar.xz",     # same as .xz
    # "tar.bz2",    # Same as .bz2
]

default_file_name = "output"
default_folder_name = "outputs"
