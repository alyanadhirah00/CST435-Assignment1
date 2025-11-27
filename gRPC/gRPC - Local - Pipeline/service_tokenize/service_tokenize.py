import time
import concurrent.futures
import grpc
import re

import protos.processing_pb2 as processing_pb2
import protos.processing_pb2_grpc as processing_pb2_grpc

# --- ADD THIS IMPORT ---
from google.protobuf import empty_pb2

# service_tokenize.py
# BEFORE: SENTIMENT_SERVICE_ADDR = 'service-sentiment:50053'
SENTIMENT_SERVICE_ADDR = 'localhost:50053'

class TokenizeService(processing_pb2_grpc.TokenizeServiceServicer):

    def Process(self, request, context):
        clean_text = request.clean_text
        filename = request.original_filename
        print(f"Tokenize Service: Received request for '{filename}'.")
        
        tokens = re.findall(r"[\w']+", clean_text)
        print(f"Tokenize Service: Split into {len(tokens)} tokens.")
        
        print(f"Tokenize Service: Pushing to Sentiment Service for '{filename}'...")
        try:
            with grpc.insecure_channel(SENTIMENT_SERVICE_ADDR) as channel:
                stub = processing_pb2_grpc.SentimentServiceStub(channel)
                sentiment_request = processing_pb2.SentimentRequest(
                    tokens=tokens,
                    original_filename=filename
                )
                # --- Fire-and-forget ---
                stub.Process(sentiment_request)

        except grpc.RpcError as e:
            print(f"Tokenize Service: ERROR - Could not push to Sentiment Service: {e.details()}")
        
        # --- Return Empty *immediately* ---
        return empty_pb2.Empty()

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    processing_pb2_grpc.add_TokenizeServiceServicer_to_server(TokenizeService(), server)
    port = "50052"
    server.add_insecure_port(f'[::]:{port}')
    print(f"Starting Tokenize Service (Async Pipeline) on port {port}...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()