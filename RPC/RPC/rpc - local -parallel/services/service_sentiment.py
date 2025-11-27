import xmlrpc.client
import xmlrpc.server
import threading
from socketserver import ThreadingMixIn

REPORT_SERVICE_ADDR = 'http://localhost:50054'

SENTIMENT_LEXICON = {
    "love":2,"great":2,"good":1,"awesome":3,"excellent":3,"nice":1,
    "best":2,"amazing":3,"fantastic":3,"wonderful":3,"delicious":2,
    "perfect":3,"hate":-2,"bad":-1,"terrible":-3,"awful":-3,
    "worst":-2,"poor":-1,"disgusting":-3,"slow":-1,"rude":-2,"unfriendly":-2
}

class ThreadingXMLRPCServer(ThreadingMixIn, xmlrpc.server.SimpleXMLRPCServer):
    pass

class SentimentService:
    def Process(self, tokens, filename):
        threading.Thread(target=self._process_in_thread, args=(tokens, filename)).start()
        return "Processing started"

    def _process_in_thread(self, tokens, filename):
        score = sum(SENTIMENT_LEXICON.get(t.lower(), 0) for t in tokens)
        sentiment = "Neutral"
        if score > 0: sentiment = "Positive"
        elif score < 0: sentiment = "Negative"
        threading.Thread(target=self.send_to_report, args=(filename, sentiment)).start()

    def send_to_report(self, filename, sentiment):
        try:
            proxy = xmlrpc.client.ServerProxy(REPORT_SERVICE_ADDR)
            proxy.Process(filename, sentiment)
        except Exception as e:
            print(f"SentimentService ERROR: {e}")

def serve():
    server = ThreadingXMLRPCServer(("localhost", 50053), allow_none=True)
    server.register_instance(SentimentService())
    print("Sentiment Service running on port 50053...")
    server.serve_forever()

if __name__ == "__main__":
    serve()
