import time
import concurrent.futures
import grpc
import re

import protos.processing_pb2 as processing_pb2
import protos.processing_pb2_grpc as processing_pb2_grpc

class TokenizeService(processing_pb2_grpc.TokenizeServiceServicer):

    def Process(self, request, context):
        clean_text = request.clean_text
        print(f"Tokenize Service: Received text to tokenize.")
        
        tokens = re.findall(r"[\w']+", clean_text)
        print(f"Tokenize Service: Split text into {len(tokens)} tokens.")
        
        # Return the specific response for this service
        return processing_pb2.TokenizeResponse(tokens=tokens)

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    processing_pb2_grpc.add_TokenizeServiceServicer_to_server(TokenizeService(), server)
    
    # --- NEW PORT ---
    port = "50062"

    server.add_insecure_port(f'[::]:{port}')
    print(f"Starting Tokenize Service (Orchestrator) on port {port}...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()