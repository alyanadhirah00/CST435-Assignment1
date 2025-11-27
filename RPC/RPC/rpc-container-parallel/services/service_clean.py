import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn
import re
import threading

TOKENIZE_SERVICE_ADDR = 'http://service-tokenize:50052/RPC2'

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class ThreadingXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class CleanService:
    def Process(self, raw_text, filename):
        """
        Cleans the raw_text and returns the cleaned text.
        """
        print(f"🧹 Clean Service: Received '{filename}'")

        # Clean text: lowercase, remove non-alphanumeric except space and apostrophe.
        text = raw_text.lower()
        text = re.sub(r"[^a-z0-9\s']+", '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        print(f"🧹 Clean Service: Text cleaned")

        # Fire-and-forget to Tokenize Service asynchronously
        threading.Thread(target=self._send_to_tokenize, args=(text, filename)).start()

        return text

    def _send_to_tokenize(self, text, filename):
        try:
            proxy = xmlrpc.client.ServerProxy(TOKENIZE_SERVICE_ADDR, allow_none=True)
            proxy.Process(text, filename)
            print(f"🧹 Clean Service: Sent to Tokenize Service '{filename}'")
        except Exception as e:
            print(f"🧹 Clean Service ERROR sending to Tokenize Service: {e}")

def serve():
    server = ThreadingXMLRPCServer(("0.0.0.0", 50051), requestHandler=RequestHandler, allow_none=True)
    server.register_instance(CleanService())
    print("Clean Service running on port 50051...")
    server.serve_forever()

if __name__ == "__main__":
    serve()
