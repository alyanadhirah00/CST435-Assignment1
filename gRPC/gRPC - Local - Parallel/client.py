import grpc
import os
import time
import concurrent.futures

import protos.processing_pb2 as processing_pb2
import protos.processing_pb2_grpc as processing_pb2_grpc

# Worker service addresses
CLEAN_SERVICE_ADDR = 'localhost:50061'
TOKENIZE_SERVICE_ADDR = 'localhost:50062'
SENTIMENT_SERVICE_ADDR = 'localhost:50063'
REPORT_SERVICE_ADDR = 'localhost:50064'


def process_file_pipeline(filename, raw_text):
    """
    Runs a single file through the entire 4-stage gRPC pipeline.
    """
    print(f"[Client] Processing '{filename}'...")
    
    try:
        # --- Step 1: Clean ---
        with grpc.insecure_channel(CLEAN_SERVICE_ADDR) as channel:
            stub = processing_pb2_grpc.CleanServiceStub(channel)
            request = processing_pb2.CleanRequest(raw_text=raw_text)
            response = stub.Process(request, timeout=10)
            clean_text = response.clean_text
        print(f"   > '{filename}': Step 1/4 Clean OK")

        # --- Step 2: Tokenize ---
        with grpc.insecure_channel(TOKENIZE_SERVICE_ADDR) as channel:
            stub = processing_pb2_grpc.TokenizeServiceStub(channel)
            request = processing_pb2.TokenizeRequest(clean_text=clean_text)
            response = stub.Process(request, timeout=10)
            tokens = response.tokens
        print(f"   > '{filename}': Step 2/4 Tokenize OK ({len(tokens)} tokens)")

        # --- Step 3: Sentiment ---
        with grpc.insecure_channel(SENTIMENT_SERVICE_ADDR) as channel:
            stub = processing_pb2_grpc.SentimentServiceStub(channel)
            request = processing_pb2.SentimentRequest(tokens=tokens)
            response = stub.Process(request, timeout=10)
            sentiment = response.sentiment
        print(f"   > '{filename}': Step 3/4 Sentiment OK ({sentiment})")

        # --- Step 4: Report ---
        with grpc.insecure_channel(REPORT_SERVICE_ADDR) as channel:
            stub = processing_pb2_grpc.ReportServiceStub(channel)
            request = processing_pb2.ReportRequest(
                original_filename=filename,
                sentiment=sentiment
            )
            response = stub.Process(request, timeout=10)
        print(f"   > '{filename}': Step 4/4 Report OK ({response.message})")
        
        return f"SUCCESS: {filename}"

    except grpc.RpcError as e:
        print(f"[Client] ERROR processing '{filename}': {e.details()}")
        return f"ERROR: {filename} ({e.details()})"
    except Exception as e:
        print(f"[Client] NON-GRPC ERROR processing '{filename}': {e}")
        return f"ERROR: {filename} ({e})"


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
                with open(os.path.join(TEXTFILE_DIR, filename), 'r') as f:
                    files_to_process.append((filename, f.read()))
                print(f"   > Loaded {filename}")
    except FileNotFoundError:
        print(f"Error: Directory not found: '{TEXTFILE_DIR}'.")
        return
    if not files_to_process:
        print(f"Error: No .txt files found in '{TEXTFILE_DIR}'.")
        return
    
    # -----------------------------
    # PROCESS FILES IN PARALLEL
    # -----------------------------
    print(f"\n--- Client: Processing {len(files_to_process)} files in parallel... ---")

    processing_start = time.perf_counter()  # Start timing **only for parallel processing**

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_file_pipeline, fn, content)
                   for fn, content in files_to_process}

        for future in concurrent.futures.as_completed(futures):
            print(f"[Client] Job Result: {future.result()}")

    processing_end = time.perf_counter()
    processing_time_sec = processing_end - processing_start
    num_files = len(files_to_process)

    # -----------------------------
    # PRINT PARALLEL THROUGHPUT
    # -----------------------------
    if processing_time_sec > 0:
        throughput = num_files / processing_time_sec
        print(f"\n--- Parallel Processing Throughput: {throughput:.2f} files/sec ---")
        print(f"--- Parallel Processing Time: {processing_time_sec*1000:.2f} ms ---")
    else:
        print("\n--- No processing time measured ---")

if __name__ == '__main__':
    run_client()
