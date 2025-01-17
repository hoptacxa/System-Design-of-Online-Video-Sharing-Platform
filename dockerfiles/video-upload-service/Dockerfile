# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy only requirements first to leverage Docker caching
COPY dockerfiles/pyserver/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY services/video-upload-service/src/app.py .

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

EXPOSE 80

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
