import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

REPORT_SERVICE_ADDR = 'http://service-report:50054'

SENTIMENT_LEXICON = {
    "love": 2, "great": 2, "good": 1, "awesome": 3, "excellent": 3, "nice": 1, "best": 2,
    "hate": -2, "bad": -1, "terrible": -3, "awful": -3, "worst": -2, "poor": -1
}

class SentimentService:
    def Process(self, tokens, filename):
        print(f"💬 Sentiment Service: Received '{filename}'.")
        print(f"   Tokens: {tokens[:5]}...")  # Show first 5 tokens

        score = sum(SENTIMENT_LEXICON.get(token.lower(), 0) for token in tokens)
        print(f"   Sentiment score: {score}")

        sentiment = "Neutral"
        if score > 0:
            sentiment = "Positive"
        elif score < 0:
            sentiment = "Negative"

        print(f"💬 Sentiment Service: Analyzed -> {sentiment}")
        print(f"   Forwarding to Report Service...")

        try:
            proxy = xmlrpc.client.ServerProxy(REPORT_SERVICE_ADDR)
            proxy.Process(filename, sentiment)
        except xmlrpc.client.Fault as e:
            print(f"Sentiment Service ERROR: {e.faultString}")

        return

def serve():
    server = ThreadedXMLRPCServer(("0.0.0.0", 50053), allow_none=True)
    instance = SentimentService()
    server.register_function(instance.Process, 'Process')
    print("Starting Sentiment Service on port 50053...")
    server.serve_forever()

if __name__ == '__main__':
    serve()
