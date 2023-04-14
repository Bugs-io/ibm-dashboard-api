#Dockerfile

# Pull base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt . 
RUN apt-get update && apt-get install -y libmagic-dev
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

VOLUME /app

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

