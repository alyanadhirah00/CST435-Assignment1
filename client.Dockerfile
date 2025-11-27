# Start from the same Python base
FROM python:3.9-slim
WORKDIR /app

# 1. Copy the client's requirements and install
COPY client_requirements.txt .
RUN pip install --no-cache-dir -r client_requirements.txt

# 2. Copy the protos and generate the gRPC code
COPY protos /app/protos
RUN python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    protos/processing.proto

# 3. Copy the client script AND its data
COPY client.py .
COPY textfile /app/textfile

# 4. The command to run when the container starts
CMD ["python", "client.py"]