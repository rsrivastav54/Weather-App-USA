# Using a light python runtime environment, found at https://hub.docker.com/_/python/tags
FROM python:3.8.19-slim-bullseye

# Working directory for the container
WORKDIR /app

# Copying the content into the container app directory
COPY . /app

# Install python library dependencies
RUN pip install -r requirements.txt

# Run the application
ENTRYPOINT ["python", "weatherApp.py"]