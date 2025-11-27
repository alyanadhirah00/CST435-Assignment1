import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import re

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

SENTIMENT_SERVICE_ADDR = 'http://service-sentiment:50053'

class TokenizeService:
    def Process(self, clean_text, filename):
        print(f"🔹 Tokenize Service: Received '{filename}'.")
        print(f"   Cleaned text: '{clean_text[:50]}...'")

        tokens = re.findall(r"[\w']+", clean_text)
        print(f"🔹 Tokenize Service: Extracted {len(tokens)} tokens -> {tokens[:5]}...")  # Show first 5 tokens
        print(f"   Forwarding to Sentiment Service...")

        try:
            proxy = xmlrpc.client.ServerProxy(SENTIMENT_SERVICE_ADDR)
            proxy.Process(tokens, filename)
        except xmlrpc.client.Fault as e:
            print(f"Tokenize Service ERROR: {e.faultString}")

        return

def serve():
    server = ThreadedXMLRPCServer(("0.0.0.0", 50052), allow_none=True)
    instance = TokenizeService()
    server.register_function(instance.Process, 'Process')
    print("Starting Tokenize Service on port 50052...")
    server.serve_forever()

if __name__ == '__main__':
    serve()
