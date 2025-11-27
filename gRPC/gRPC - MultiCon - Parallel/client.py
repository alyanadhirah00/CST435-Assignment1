import grpc
import os
import time
import concurrent.futures
from datetime import datetime
import pytz

import protos.processing_pb2 as processing_pb2
import protos.processing_pb2_grpc as processing_pb2_grpc

# --- 1. Define NEW addresses for all 4 workers ---
CLEAN_SERVICE_ADDR = 'service-clean:50061'
TOKENIZE_SERVICE_ADDR = 'service-tokenize:50062'
SENTIMENT_SERVICE_ADDR = 'service-sentiment:50063'
REPORT_SERVICE_ADDR = 'service-report:50064'


# --- 2. Main pipeline function for a single file ---
def process_file_pipeline(filename, raw_text):
    """
    Runs a single file through the entire 4-stage gRPC pipeline.
    """
    print(f"[Client] Processing '{filename}'...")
    try:
        # Step 1: Clean Service
        with grpc.insecure_channel(CLEAN_SERVICE_ADDR) as channel:
            stub = processing_pb2_grpc.CleanServiceStub(channel)
            request = processing_pb2.CleanRequest(raw_text=raw_text)
            response = stub.Process(request, timeout=10)
            clean_text = response.clean_text
        print(f" > '{filename}': Step 1/4 Clean OK")

        # Step 2: Tokenize Service
        with grpc.insecure_channel(TOKENIZE_SERVICE_ADDR) as channel:
            stub = processing_pb2_grpc.TokenizeServiceStub(channel)
            request = processing_pb2.TokenizeRequest(clean_text=clean_text)
            response = stub.Process(request, timeout=10)
            tokens = response.tokens
        print(f" > '{filename}': Step 2/4 Tokenize OK ({len(tokens)} tokens)")

        # Step 3: Sentiment Service
        with grpc.insecure_channel(SENTIMENT_SERVICE_ADDR) as channel:
            stub = processing_pb2_grpc.SentimentServiceStub(channel)
            request = processing_pb2.SentimentRequest(tokens=tokens)
            response = stub.Process(request, timeout=10)
            sentiment = response.sentiment
        print(f" > '{filename}': Step 3/4 Sentiment OK ({sentiment})")

        # Step 4: Report Service
        with grpc.insecure_channel(REPORT_SERVICE_ADDR) as channel:
            stub = processing_pb2_grpc.ReportServiceStub(channel)
            request = processing_pb2.ReportRequest(original_filename=filename, sentiment=sentiment)
            response = stub.Process(request, timeout=10)
        print(f" > '{filename}': Step 4/4 Report OK ({response.message})")

        return f"SUCCESS: {filename}"

    except grpc.RpcError as e:
        print(f"[Client] ERROR processing '{filename}': {e.details()}")
        return f"ERROR: {filename} ({e.details()})"
    except Exception as e:
        print(f"[Client] NON-GRPC ERROR processing '{filename}': {e}")
        return f"ERROR: {filename} ({e})"


# --- 3. Main client function ---
def run_client():
    print("--- Client: Waiting 5s for services to start... ---")
    time.sleep(5)
    print("--- Client: Starting Orchestrator ---")

    TEXTFILE_DIR = "textfile"
    files_to_process = []

    print(f"--- Client: Loading files from '{TEXTFILE_DIR}' directory ---")
    try:
        for filename in os.listdir(TEXTFILE_DIR):
            if filename.endswith(".txt"):
                filepath = os.path.join(TEXTFILE_DIR, filename)
                with open(filepath, 'r', encoding="utf-8") as f:
                    content = f.read()
                files_to_process.append((filename, content))
                print(f" > Loaded {filename}")
    except FileNotFoundError:
        print(f"Error: Directory not found: '{TEXTFILE_DIR}'.")
        return

    if not files_to_process:
        print(f"Error: No .txt files found in '{TEXTFILE_DIR}'.")
        return

    # --- 4. Process all files in parallel ---
    print(f"\n--- Client: Processing {len(files_to_process)} files in parallel... ---")
    total_start_time = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_file_pipeline, filename, content)
                   for filename, content in files_to_process}

        for future in concurrent.futures.as_completed(futures):
            print(f"[Client] Job Result: {future.result()}")

    total_end_time = time.perf_counter()

    # --- 5. Timestamp for when submission finishes ---
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    client_submit_time = datetime.now(tz)
    print(f"\n[Client] Submit Time: {client_submit_time.strftime('%d/%m/%Y %H:%M:%S.%f')}")

    # --- 6. Summary ---
    total_time_sec = total_end_time - total_start_time
    num_files = len(files_to_process)

    print(f"\n--- Finished all {num_files} files in {total_time_sec * 1000:.2f} ms ---")
    if total_time_sec > 0:
        throughput = num_files / total_time_sec
        print(f"--- Throughput: {throughput:.2f} files per second ---")

    print("--- Client: Orchestration complete. Check the 'reports/results.csv' file! ---")


if __name__ == '__main__':
    run_client()
