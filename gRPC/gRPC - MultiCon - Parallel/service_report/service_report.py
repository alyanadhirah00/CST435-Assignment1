import time
import concurrent.futures
import grpc
import os

import protos.processing_pb2 as processing_pb2
import protos.processing_pb2_grpc as processing_pb2_grpc

REPORTS_DIR = "/app/reports"
RESULTS_FILE = os.path.join(REPORTS_DIR, "results.csv")

class ReportService(processing_pb2_grpc.ReportServiceServicer):

    def __init__(self):
        print(f"Report Service: Ensuring directory exists: {REPORTS_DIR}")
        os.makedirs(REPORTS_DIR, exist_ok=True)
        if not os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'w') as f:
                f.write("filename,sentiment\n")
                print("Report Service: Created new results.csv with header.")

    def Process(self, request, context):
        filename = request.original_filename
        sentiment = request.sentiment
        print(f"Report Service: Received request to log: {filename} -> {sentiment}")
        
        try:
            with open(RESULTS_FILE, 'a') as f:
                f.write(f"{filename},{sentiment}\n")
            print(f"Report Service: Successfully logged to {RESULTS_FILE}")
            
            # Return the specific response for this service
            return processing_pb2.ReportResponse(
                success=True,
                message=f"Logged {filename} as {sentiment}"
            )
        except Exception as e:
            print(f"Report Service: FAILED to write to file: {e}")
            return processing_pb2.ReportResponse(success=False, message=str(e))

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    processing_pb2_grpc.add_ReportServiceServicer_to_server(ReportService(), server)
    
    # --- NEW PORT ---
    port = "50064"
    
    server.add_insecure_port(f'[::]:{port}')
    print(f"Starting Report Service (Orchestrator) on port {port}...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()