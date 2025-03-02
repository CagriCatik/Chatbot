# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required by Poetry and your project
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy only the Poetry files to leverage Docker cache
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry to create the virtual environment inside the container and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of your application code
COPY . /src

# Specify the command to run your application
# Replace "your_script.py" with the entrypoint of your application
CMD ["python", "run.py"]
