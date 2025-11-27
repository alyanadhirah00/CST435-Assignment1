import time
import concurrent.futures
import grpc
import re

import protos.processing_pb2 as processing_pb2
import protos.processing_pb2_grpc as processing_pb2_grpc

# --- ADD THIS IMPORT ---
from google.protobuf import empty_pb2

# service_clean.py
# BEFORE: TOKENIZE_SERVICE_ADDR = 'service-tokenize:50052'
TOKENIZE_SERVICE_ADDR = 'localhost:50052'

class CleanService(processing_pb2_grpc.CleanServiceServicer):

    def Process(self, request, context):
        raw_text = request.raw_text
        filename = request.original_filename
        print(f"Clean Service: Received '{filename}'.")
        
        text = raw_text.lower()
        text = re.sub(r"[^a-z0-9\s']+", '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"Clean Service: Text cleaned.")
        
        print(f"Clean Service: Pushing to Tokenize Service for '{filename}'...")
        try:
            with grpc.insecure_channel(TOKENIZE_SERVICE_ADDR) as channel:
                stub = processing_pb2_grpc.TokenizeServiceStub(channel)
                tokenize_request = processing_pb2.TokenizeRequest(
                    clean_text=text,
                    original_filename=filename
                )
                
                # --- THIS IS THE KEY CHANGE ---
                # We call Process, but we don't save or return the result.
                # This is a "fire-and-forget" call.
                stub.Process(tokenize_request) 
                
        except grpc.RpcError as e:
            # In a real app, you'd need a way to handle this (e.g., a retry queue)
            print(f"Clean Service: ERROR - Could not push to Tokenize Service: {e.details()}")
        
        # --- We return Empty *immediately* ---
        # We don't wait for the rest of the pipeline.
        return empty_pb2.Empty()

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    processing_pb2_grpc.add_CleanServiceServicer_to_server(CleanService(), server)
    port = "50051"
    server.add_insecure_port(f'[::]:{port}')
    print(f"Starting Clean Service (Async Pipeline) on port {port}...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()