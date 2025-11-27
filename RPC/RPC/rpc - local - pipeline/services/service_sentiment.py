import xmlrpc.client
import xmlrpc.server

REPORT_SERVICE_ADDR = 'http://localhost:50054'

# Expanded lexicon for better sentiment detection
SENTIMENT_LEXICON = {
    "love":2, "great":2, "good":1, "awesome":3, "excellent":3, "nice":1, "best":2,
    "amazing":3, "fantastic":3, "wonderful":3, "delicious":2, "perfect":3,
    "hate":-2, "bad":-1, "terrible":-3, "awful":-3, "worst":-2, "poor":-1, "disgusting":-3,
    "slow":-1, "rude":-2, "unfriendly":-2
}

class SentimentService:
    def Process(self, tokens, filename):
        print(f"Sentiment Service: Received {len(tokens)} tokens for '{filename}'.")

        # Kira score
        score = sum(SENTIMENT_LEXICON.get(token.lower(), 0) for token in tokens)

        # Tentukan sentiment
        sentiment = "Neutral"
        if score > 0:
            sentiment = "Positive"
        elif score < 0:
            sentiment = "Negative"

        # Debug print
        print(f"Tokens: {tokens}")
        print(f"Score: {score} -> Sentiment: {sentiment}")

        # Push ke Report Service
        try:
            proxy = xmlrpc.client.ServerProxy(REPORT_SERVICE_ADDR)
            proxy.Process(filename, sentiment)  # fire-and-forget
        except xmlrpc.client.Fault as e:
            print(f"Sentiment Service: ERROR - {e.faultString}")
        return

def serve():
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 50053), allow_none=True)
    instance = SentimentService()
    server.register_function(instance.Process, 'Process')
    print(f"Starting Sentiment Service on port 50053...")
    server.serve_forever()

if __name__ == '__main__':
    serve()
