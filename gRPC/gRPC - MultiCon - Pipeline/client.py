import grpc
import os
import time
import concurrent.futures

import protos.processing_pb2 as processing_pb2
import protos.processing_pb2_grpc as processing_pb2_grpc

# Address of the cleaning service
CLEAN_SERVICE_ADDR = 'service-clean:50051'


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

            # Fire-and-forget call (client doesn't wait for result)
            stub.Process(request, timeout=10)

            return f"SUBMITTED: {filename}"

    except grpc.RpcError as e:
        print(f"[Client] ERROR submitting '{filename}': {e.details()}")
        return f"ERROR: {filename} ({e.details()})"

    except Exception as e:
        print(f"[Client] NON-GRPC ERROR submitting '{filename}': {e}")
        return f"ERROR: {filename} ({e})"


def run_client():
    print("--- Client: Waiting 5s for services to start... ---")
    time.sleep(5)

    print("--- Client: Starting Client ---")

    TEXTFILE_DIR = "textfile"
    files_to_process = []

    print(f"--- Client: Loading files from '{TEXTFILE_DIR}' directory ---")

    # Load all .txt files
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

    # Submit jobs in parallel
    print(f"\n--- Client: Submitting {len(files_to_process)} files to pipeline... ---")
    total_start_time = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(push_file_to_pipeline, filename, content)
            for filename, content in files_to_process
        }

        for future in concurrent.futures.as_completed(futures):
            print(f"[Client] Job Status: {future.result()}")

    total_end_time = time.perf_counter()
    elapsed_sec = total_end_time - total_start_time

    # Print time taken
    print(f"\n--- Finished submitting {len(files_to_process)} files in "
          f"{elapsed_sec * 1000:.2f} ms ---")

    # Calculate and print throughput
    throughput = len(files_to_process) / elapsed_sec
    print(f"--- Throughput: {throughput:.2f} files per second ---")

    print("--- Client: All jobs are now processing in the background. ---")
    print("--- Client: Monitor worker logs or check 'reports/results.csv' for output. ---")

if __name__ == '__main__':
    run_client()
