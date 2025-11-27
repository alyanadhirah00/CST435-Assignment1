FROM python:3.9-slim
WORKDIR /app

# Copy this service's requirements
COPY service_tokenize/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .proto file
COPY protos /app/protos

# Generate the gRPC code
RUN python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    protos/processing.proto

# Copy this service's Python script
COPY service_tokenize/service_tokenize.py .

# Expose our new port
EXPOSE 50052

# Run the service
CMD ["python", "service_tokenize.py"]