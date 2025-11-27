import xmlrpc.client
import xmlrpc.server
import re

SENTIMENT_SERVICE_ADDR = 'http://localhost:50053'

class TokenizeService:
    def Process(self, clean_text, filename):
        print(f"Tokenize Service: Received request for '{filename}'.")

        # Tokenization
        tokens = re.findall(r"[\w']+", clean_text)
        print(f"Tokenize Service: Split into {len(tokens)} tokens: {tokens}")

        print(f"Tokenize Service: Pushing to Sentiment Service for '{filename}'...")
        try:
            proxy = xmlrpc.client.ServerProxy(SENTIMENT_SERVICE_ADDR)
            proxy.Process(tokens, filename)  # fire-and-forget
        except xmlrpc.client.Fault as e:
            print(f"Tokenize Service: ERROR - {e.faultString}")
        return

def serve():
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 50052), allow_none=True)
    instance = TokenizeService()
    server.register_function(instance.Process, 'Process')
    print(f"Starting Tokenize Service on port 50052...")
    server.serve_forever()

if __name__ == '__main__':
    serve()
