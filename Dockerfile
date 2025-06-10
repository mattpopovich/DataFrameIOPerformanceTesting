# Get current python image
#   (use -bullseye variants on local arm64/Apple Silicon)
FROM python:3.13.4-bullseye

# Update image
RUN apt-get update && apt-get upgrade -y

# Python pandas for DataFrame handling
RUN pip3 install --upgrade pandas
