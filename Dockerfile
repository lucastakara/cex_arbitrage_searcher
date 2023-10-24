# Use an official Python runtime as the parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app/

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install uWSGI
RUN pip install uwsgi


# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "--mount", "/=app:app"]
