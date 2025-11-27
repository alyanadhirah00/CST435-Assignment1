# Base image
FROM python:3.11-slim


# Set working directory
WORKDIR /app


# Install minimal deps (if any)
# RUN pip install --no-cache-dir xmlrpc


# Copy all code
COPY . /app


# Expose default ports (containers publish via compose)
EXPOSE 50051 50052 50053 50054


# Default command (overridden by compose)
CMD ["python3", "client.py"]