import time
import concurrent.futures
import grpc
import re

import protos.processing_pb2 as processing_pb2
import protos.processing_pb2_grpc as processing_pb2_grpc

class CleanService(processing_pb2_grpc.CleanServiceServicer):

    def Process(self, request, context):
        raw_text = request.raw_text
        print(f"Clean Service: Received raw text.")
        
        text = raw_text.lower()
        text = re.sub(r"[^a-z0-9\s']+", '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"Clean Service: Text cleaned.")
        
        # Return the specific response for this service
        return processing_pb2.CleanResponse(clean_text=text)

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    processing_pb2_grpc.add_CleanServiceServicer_to_server(CleanService(), server)
    
    # --- NEW PORT ---
    port = "50061"
    
    server.add_insecure_port(f'[::]:{port}')
    print(f"Starting Clean Service (Orchestrator) on port {port}...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()