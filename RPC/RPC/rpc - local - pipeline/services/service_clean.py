import xmlrpc.client
import xmlrpc.server
import re

TOKENIZE_SERVICE_ADDR = 'http://localhost:50052'

class CleanService:
    def Process(self, raw_text, filename):
        print(f"Clean Service: Received '{filename}'.")

        # Lowercase dan buang punctuation
        text = raw_text.lower()
        text = re.sub(r"[^a-z0-9\s']+", '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"Clean Service: Text cleaned.")

        print(f"Clean Service: Pushing to Tokenize Service for '{filename}'...")
        try:
            proxy = xmlrpc.client.ServerProxy(TOKENIZE_SERVICE_ADDR)
            proxy.Process(text, filename)  # fire-and-forget
        except xmlrpc.client.Fault as e:
            print(f"Clean Service: ERROR - {e.faultString}")
        return

def serve():
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 50051), allow_none=True)
    instance = CleanService()
    server.register_function(instance.Process, 'Process')
    print(f"Starting Clean Service on port 50051...")
    server.serve_forever()

if __name__ == '__main__':
    serve()
