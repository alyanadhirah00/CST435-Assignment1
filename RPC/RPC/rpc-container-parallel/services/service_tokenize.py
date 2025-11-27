import re
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class ThreadingXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class TokenizeService:
    def Process(self, clean_text, filename):
        tokens = re.findall(r"[\\w']+", clean_text)
        return tokens


def serve():
    server = ThreadingXMLRPCServer(("0.0.0.0", 50052), requestHandler=RequestHandler, allow_none=True)
    server.register_instance(TokenizeService())
    print("Tokenize Service running on port 50052...")
    server.serve_forever()


if __name__ == "__main__":
    serve()
