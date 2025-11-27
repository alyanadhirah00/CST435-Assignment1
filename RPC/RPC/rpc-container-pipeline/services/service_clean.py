import xmlrpc.client
import re
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

TOKENIZE_SERVICE_ADDR = 'http://service-tokenize:50052'

class CleanService:
    def Process(self, raw_text, filename):
        print(f"🧹 Clean Service: Received '{filename}'.")
        print(f"   Input text: '{raw_text[:50]}...'")  # Show first 50 chars for demo

        # Clean text
        text = raw_text.lower()
        text = re.sub(r"[^a-z0-9\s']+", '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"🧹 Clean Service: Text cleaned -> '{text[:50]}...'")
        print(f"   Forwarding to Tokenize Service...")

        # Fire-and-forget to Tokenize Service
        try:
            proxy = xmlrpc.client.ServerProxy(TOKENIZE_SERVICE_ADDR)
            proxy.Process(text, filename)
        except xmlrpc.client.Fault as e:
            print(f"Clean Service ERROR: {e.faultString}")

        return

def serve():
    server = ThreadedXMLRPCServer(("0.0.0.0", 50051), allow_none=True)
    instance = CleanService()
    server.register_function(instance.Process, 'Process')
    print("Starting Clean Service on port 50051...")
    server.serve_forever()

if __name__ == '__main__':
    serve()
