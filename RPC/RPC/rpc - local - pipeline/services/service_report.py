import xmlrpc.server
import os

REPORTS_DIR = "reports"
RESULTS_FILE = os.path.join(REPORTS_DIR, "results.csv")

class ReportService:
    def __init__(self):
        os.makedirs(REPORTS_DIR, exist_ok=True)
        if not os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'w') as f:
                f.write("filename,sentiment\n")
            print(f"Report Service: Created results.csv")

    def Process(self, filename, sentiment):
        print(f"Report Service: Logging {filename} -> {sentiment}")
        try:
            with open(RESULTS_FILE, 'a') as f:
                f.write(f"{filename},{sentiment}\n")
            print(f"Report Service: Successfully logged to {RESULTS_FILE}")
        except Exception as e:
            print(f"Report Service: FAILED - {e}")
        return

def serve():
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 50054), allow_none=True)
    instance = ReportService()
    server.register_function(instance.Process, 'Process')
    print(f"Starting Report Service on port 50054...")
    server.serve_forever()

if __name__ == '__main__':
    serve()
