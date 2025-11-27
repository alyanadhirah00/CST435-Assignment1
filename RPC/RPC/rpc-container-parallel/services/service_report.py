import os
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
RESULTS_FILE = os.path.join(REPORTS_DIR, "results.csv")

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class ThreadingXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class ReportService:
    def __init__(self):
        os.makedirs(REPORTS_DIR, exist_ok=True)
        if not os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'w') as f:
                f.write("filename,sentiment\n")
            print("📑 Report Service: Created results.csv")

    def Process(self, filename, sentiment):
        threading.Thread(target=self._process_in_thread, args=(filename, sentiment)).start()
        return "Processing started"

    def _process_in_thread(self, filename, sentiment):
        print(f"📑 Report Service: Logging {filename} -> {sentiment}")
        try:
            with open(RESULTS_FILE, 'a') as f:
                f.write(f"{filename},{sentiment}\n")
            print(f"📑 Report Service: Successfully logged")
        except Exception as e:
            print(f"Report Service ERROR: {e}")

def serve():
    server = ThreadingXMLRPCServer(("0.0.0.0", 50054), requestHandler=RequestHandler, allow_none=True)
    server.register_instance(ReportService())
    print("Report Service running on port 50054...")
    server.serve_forever()

if __name__ == "__main__":
    serve()
