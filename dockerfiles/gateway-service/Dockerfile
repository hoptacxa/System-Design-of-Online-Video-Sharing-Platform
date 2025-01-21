# Use a lightweight Python base image
FROM python:3.11-slim
RUN apt-get update && apt-get install gcc -y

# Set the working directory
WORKDIR /app

# Copy only requirements first to leverage Docker caching
COPY dockerfiles/pyserver/requirements.txt .
COPY services/gateway/requirements.txt application-requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt -r application-requirements.txt

# Copy the rest of the application code
COPY services/gateway/src/ ./src/

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=./src/

EXPOSE 80
