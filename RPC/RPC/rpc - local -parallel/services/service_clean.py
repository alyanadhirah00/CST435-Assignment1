import xmlrpc.client
import xmlrpc.server
import re
import threading
from socketserver import ThreadingMixIn

TOKENIZE_SERVICE_ADDR = 'http://localhost:50052'

class ThreadingXMLRPCServer(ThreadingMixIn, xmlrpc.server.SimpleXMLRPCServer):
    pass

class CleanService:
    def Process(self, raw_text, filename):
        threading.Thread(target=self._process_in_thread, args=(raw_text, filename)).start()
        return "Processing started"

    def _process_in_thread(self, raw_text, filename):
        text = raw_text.lower()
        text = re.sub(r"[^a-z0-9\s']+", '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        threading.Thread(target=self.send_to_tokenize, args=(text, filename)).start()

    def send_to_tokenize(self, text, filename):
        try:
            proxy = xmlrpc.client.ServerProxy(TOKENIZE_SERVICE_ADDR)
            proxy.Process(text, filename)
        except Exception as e:
            print(f"CleanService ERROR: {e}")

def serve():
    server = ThreadingXMLRPCServer(("localhost", 50051), allow_none=True)
    server.register_instance(CleanService())
    print("Clean Service running on port 50051...")
    server.serve_forever()

if __name__ == "__main__":
    serve()
