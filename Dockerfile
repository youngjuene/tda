# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install GDAL and its development files
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    gdal-bin \
    python3-gdal

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required libraries
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to the Python interpreter
ENTRYPOINT ["python"]