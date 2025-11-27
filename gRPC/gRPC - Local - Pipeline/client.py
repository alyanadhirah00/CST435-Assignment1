import grpc
import os
import time
import concurrent.futures

import protos.processing_pb2 as processing_pb2
import protos.processing_pb2_grpc as processing_pb2_grpc

CLEAN_SERVICE_ADDR = 'localhost:50051'


def push_file_to_pipeline(filename, raw_text):
    """
    Pushes a single file into the 'fire-and-forget' pipeline.
    """
    print(f"[Client] Pushing '{filename}' to the pipeline...")
    
    try:
        with grpc.insecure_channel(CLEAN_SERVICE_ADDR) as channel:
            stub = processing_pb2_grpc.CleanServiceStub(channel)
            request = processing_pb2.CleanRequest(
                raw_text=raw_text,
                original_filename=filename
            )
            # Fire-and-forget call
            stub.Process(request, timeout=10)
            
            return f"SUBMITTED: {filename}"

    except grpc.RpcError as e:
        print(f"[Client] ERROR submitting '{filename}': {e.details()}")
        return f"ERROR: {filename} ({e.details()})"
    except Exception as e:
        print(f"[Client] NON-GRPC ERROR submitting '{filename}': {e}")
        return f"ERROR: {filename} ({e})"


def run_client():

    # === TOTAL TIME START ===
    total_start_ms = time.perf_counter() * 1000
    # =========================

    print("--- Client: Waiting 5s for services to start... ---")
    time.sleep(5)

    print("--- Client: Starting Client ---")
    
    TEXTFILE_DIR = "textfile"
    files_to_process = []
    
    print(f"--- Client: Loading files from '{TEXTFILE_DIR}' directory ---")
    try:
        for filename in os.listdir(TEXTFILE_DIR):
            if filename.endswith(".txt"):
                filepath = os.path.join(TEXTFILE_DIR, filename)
                with open(filepath, 'r') as f:
                    content = f.read()
                    files_to_process.append((filename, content))
                    print(f"   > Loaded {filename}")
    except FileNotFoundError:
        print(f"Error: Directory not found: '{TEXTFILE_DIR}'.")
        return
    if not files_to_process:
        print(f"Error: No .txt files found in '{TEXTFILE_DIR}'.")
        return
    
    # ----------------------------------------------------
    # SUBMISSION PHASE
    # ----------------------------------------------------
    print(f"\n--- Client: Submitting {len(files_to_process)} files to pipeline... ---")
    submit_start_ms = time.perf_counter() * 1000
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(push_file_to_pipeline, filename, content)
                   for filename, content in files_to_process}
        
        for future in concurrent.futures.as_completed(futures):
            print(f"[Client] Job Status: {future.result()}")

    submit_end_ms = time.perf_counter() * 1000
    submit_elapsed_sec = (submit_end_ms - submit_start_ms) / 1000


    # ----------------------------------------------------
    # WAIT FOR PIPELINE TO COMPLETE
    # ----------------------------------------------------
    print("\n--- Client: Waiting for pipeline to finish ---")
    expected_results = len(files_to_process)
    results_path = os.path.join("reports", "results.csv")

    process_start_ms = time.time() * 1000

    while True:
        if os.path.exists(results_path):
            try:
                with open(results_path, "r") as f:
                    row_count = sum(1 for _ in f)
                # Adjust for header if needed
            except:
                row_count = 0

            if row_count >= expected_results:
                break

        time.sleep(0.1)

    process_end_ms = time.time() * 1000
    pipeline_elapsed_sec = (process_end_ms - process_start_ms) / 1000

    # ----------------------------------------------------
    # Calculate pipeline throughput
    # ----------------------------------------------------
    pipeline_throughput = len(files_to_process) / pipeline_elapsed_sec
    print(f"\n--- Pipeline Throughput: {pipeline_throughput:.2f} files/sec ---")

if __name__ == '__main__':
    run_client()
