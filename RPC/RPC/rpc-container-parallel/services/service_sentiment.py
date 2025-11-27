import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn
import threading

REPORT_SERVICE_ADDR = 'http://service-report:50054/RPC2'

SENTIMENT_LEXICON = {
    "love":2, "great":2, "good":1, "awesome":3, "excellent":3, "nice":1, "best":2,
    "amazing":3, "fantastic":3, "wonderful":3, "delicious":2, "perfect":3,
    "hate":-2, "bad":-1, "terrible":-3, "awful":-3, "worst":-2, "poor":-1, "disgusting":-3,
    "slow":-1, "rude":-2, "unfriendly":-2
}

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class ThreadingXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class SentimentService:
    def Process(self, tokens, filename):
        threading.Thread(target=self._process_in_thread, args=(tokens, filename)).start()
        return "Processing started"

    def _process_in_thread(self, tokens, filename):
        score = sum(SENTIMENT_LEXICON.get(token.lower(), 0) for token in tokens)
        sentiment = "Neutral"
        if score > 0:
            sentiment = "Positive"
        elif score < 0:
            sentiment = "Negative"
        print(f"😊 Sentiment Service: {filename} -> {sentiment}")

        def send_to_report():
            try:
                proxy = xmlrpc.client.ServerProxy(REPORT_SERVICE_ADDR, allow_none=True)
                proxy.Process(filename, sentiment)
            except Exception as e:
                print(f"Sentiment Service ERROR: {e}")

        threading.Thread(target=send_to_report).start()

def serve():
    server = ThreadingXMLRPCServer(("0.0.0.0", 50053), requestHandler=RequestHandler, allow_none=True)
    server.register_instance(SentimentService())
    print("Sentiment Service running on port 50053...")
    server.serve_forever()

if __name__ == "__main__":
    serve()
