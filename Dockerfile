#Dockerfile

# Pull base image
FROM python:3.10-slim
# Set working directory
WORKDIR /server

# Install dependencies
COPY requirements.txt . 
RUN apt-get update && apt-get install -y libmagic-dev
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 app.interface.api:app
