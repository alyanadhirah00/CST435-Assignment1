import xmlrpc.server
import threading
import os
from socketserver import ThreadingMixIn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
RESULTS_FILE = os.path.join(REPORTS_DIR, "results.csv")

class ThreadingXMLRPCServer(ThreadingMixIn, xmlrpc.server.SimpleXMLRPCServer):
    pass

class ReportService:
    def __init__(self):
        os.makedirs(REPORTS_DIR, exist_ok=True)
        if not os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE,'w') as f:
                f.write("filename,sentiment\n")

    def Process(self, filename, sentiment):
        threading.Thread(target=self._process_in_thread, args=(filename, sentiment)).start()
        return "Processing started"

    def _process_in_thread(self, filename, sentiment):
        with open(RESULTS_FILE,'a') as f:
            f.write(f"{filename},{sentiment}\n")

def serve():
    server = ThreadingXMLRPCServer(("localhost", 50054), allow_none=True)
    server.register_instance(ReportService())
    print("Report Service running on port 50054...")
    server.serve_forever()

if __name__ == "__main__":
    serve()
