# Base image containing Python runtime
FROM python:3.12-slim

# Copy application files from host to container
# NOTES: This copies all files in this file's current directory, then whe the container is
# generated, it creates a directory called /app/ within the container.
COPY . /app/

# Set the default working directory of the container
WORKDIR /app

# Install dependencies listed in requirements.txt
# How does this text file work???
RUN pip install -r requirements.txt

# We need to define the command to launch when we are going to run the image.
# The following command will execute "python ./main.py".
CMD [ "python", "./__main__.py" ]
