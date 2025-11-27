import os
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

REPORTS_DIR = "reports"
RESULTS_FILE = os.path.join(REPORTS_DIR, "results.csv")

class ReportService:
    def __init__(self):
        os.makedirs(REPORTS_DIR, exist_ok=True)
        if not os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'w') as f:
                f.write("filename,sentiment\n")
            print("📄 Report Service: Created results.csv")

    def Process(self, filename, sentiment):
        print(f"📄 Report Service: Received '{filename}' with sentiment '{sentiment}'.")
        print(f"   Writing to results.csv...")
        with open(RESULTS_FILE, 'a') as f:
            f.write(f"{filename},{sentiment}\n")
        print(f"📄 Report Service: Logged successfully.")
        return

def serve():
    server = ThreadedXMLRPCServer(("0.0.0.0", 50054), allow_none=True)
    instance = ReportService()
    server.register_function(instance.Process, 'Process')
    print("Starting Report Service on port 50054...")
    server.serve_forever()

if __name__ == '__main__':
    serve()
