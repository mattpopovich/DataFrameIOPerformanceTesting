# Get current python image
#   (use -bullseye variants on local arm64/Apple Silicon)
FROM python:3.13.4-bullseye

# Update image
RUN apt-get update && apt-get upgrade -y

# Python pandas for DataFrame handling
RUN pip3 install --upgrade pandas

# Apache Arrow Python binding
RUN pip3 install --upgrade pyarrow

# Pytables for .h5 files
RUN pip3 install --upgrade tables

# Pretty printing tables
RUN pip3 install --upgrade tabulate rich

# Progress bar
RUN pip3 install --upgrade tqdm

# Zstandard compression library
RUN pip3 install --upgrade zstandard

# Unit testing
RUN pip3 install --upgrade pytest

# Python implementation of Apache Parquet Format
RUN pip3 install --upgrade fastparquet

# Set working directory
WORKDIR /app

# Copy my project code into the image
COPY . .
