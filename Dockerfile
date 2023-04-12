#Dockerfile

# Pull base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y libmagic-dev
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy project
COPY . .
