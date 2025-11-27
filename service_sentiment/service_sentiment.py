import time
import concurrent.futures
import grpc

import protos.processing_pb2 as processing_pb2
import protos.processing_pb2_grpc as processing_pb2_grpc

SENTIMENT_LEXICON = {
    "love": 2, "great": 2, "good": 1, "awesome": 3, "excellent": 3, "nice": 1, "best": 2,
    "hate": -2, "bad": -1, "terrible": -3, "awful": -3, "worst": -2, "poor": -1
}

class SentimentService(processing_pb2_grpc.SentimentServiceServicer):

    def Process(self, request, context):
        tokens = request.tokens
        print(f"Sentiment Service: Received {len(tokens)} tokens.")
        
        score = 0
        for token in tokens:
            score += SENTIMENT_LEXICON.get(token.lower(), 0)

        sentiment = "Neutral"
        if score > 0:
            sentiment = "Positive"
        elif score < 0:
            sentiment = "Negative"
        print(f"Sentiment Service: Calculated final score: {score} -> {sentiment}")
        
        # Return the specific response for this service
        return processing_pb2.SentimentResponse(sentiment=sentiment)

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    processing_pb2_grpc.add_SentimentServiceServicer_to_server(SentimentService(), server)
    
    # --- NEW PORT ---
    port = "50063"

    server.add_insecure_port(f'[::]:{port}')
    print(f"Starting Sentiment Service (Orchestrator) on port {port}...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()