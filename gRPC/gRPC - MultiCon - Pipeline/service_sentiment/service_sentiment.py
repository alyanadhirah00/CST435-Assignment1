import time
import concurrent.futures
import grpc

import protos.processing_pb2 as processing_pb2
import protos.processing_pb2_grpc as processing_pb2_grpc

# --- ADD THIS IMPORT ---
from google.protobuf import empty_pb2

REPORT_SERVICE_ADDR = 'service-report:50054'

# (Your SENTIMENT_LEXICON ... no change)
SENTIMENT_LEXICON = {
    "love": 2, "great": 2, "good": 1, "awesome": 3, "excellent": 3, "nice": 1, "best": 2,
    "hate": -2, "bad": -1, "terrible": -3, "awful": -3, "worst": -2, "poor": -1
}

class SentimentService(processing_pb2_grpc.SentimentServiceServicer):

    def Process(self, request, context):
        tokens = request.tokens
        filename = request.original_filename
        print(f"Sentiment Service: Received {len(tokens)} tokens for '{filename}'.")
        
        score = 0
        for token in tokens:
            score += SENTIMENT_LEXICON.get(token.lower(), 0)
        
        sentiment = "Neutral"
        if score > 0:
            sentiment = "Positive"
        elif score < 0:
            sentiment = "Negative"
        print(f"Sentiment Service: Calculated score {score} -> {sentiment}")
        
        print(f"Sentiment Service: Pushing to Report Service for '{filename}'...")
        try:
            with grpc.insecure_channel(REPORT_SERVICE_ADDR) as channel:
                stub = processing_pb2_grpc.ReportServiceStub(channel)
                report_request = processing_pb2.ReportRequest(
                    original_filename=filename,
                    sentiment=sentiment
                )
                # --- Fire-and-forget ---
                stub.Process(report_request)

        except grpc.RpcError as e:
            print(f"Sentiment Service: ERROR - Could not push to Report Service: {e.details()}")
        
        # --- Return Empty *immediately* ---
        return empty_pb2.Empty()

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    processing_pb2_grpc.add_SentimentServiceServicer_to_server(SentimentService(), server)
    port = "50053"
    server.add_insecure_port(f'[::]:{port}')
    print(f"Starting Sentiment Service (Async Pipeline) on port {port}...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()