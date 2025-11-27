import xmlrpc.client
import xmlrpc.server
import re
import threading
from socketserver import ThreadingMixIn

SENTIMENT_SERVICE_ADDR = 'http://localhost:50053'

class ThreadingXMLRPCServer(ThreadingMixIn, xmlrpc.server.SimpleXMLRPCServer):
    pass

class TokenizeService:
    def Process(self, clean_text, filename):
        threading.Thread(target=self._process_in_thread, args=(clean_text, filename)).start()
        return "Processing started"

    def _process_in_thread(self, clean_text, filename):
        tokens = re.findall(r"[\w']+", clean_text)
        threading.Thread(target=self.send_to_sentiment, args=(tokens, filename)).start()

    def send_to_sentiment(self, tokens, filename):
        try:
            proxy = xmlrpc.client.ServerProxy(SENTIMENT_SERVICE_ADDR)
            proxy.Process(tokens, filename)
        except Exception as e:
            print(f"TokenizeService ERROR: {e}")

def serve():
    server = ThreadingXMLRPCServer(("localhost", 50052), allow_none=True)
    server.register_instance(TokenizeService())
    print("Tokenize Service running on port 50052...")
    server.serve_forever()

if __name__ == "__main__":
    serve()
