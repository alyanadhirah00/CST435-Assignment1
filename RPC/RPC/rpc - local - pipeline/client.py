import glob
import time
import xmlrpc.client
import os

# Service addresses
CLEAN_SERVICE_ADDR = "http://localhost:50051"
REPORT_SERVICE_ADDR = "http://localhost:50054"

# Folder with text files
TEXT_FILES_DIR = "textfile"
files = glob.glob(f"{TEXT_FILES_DIR}/*.txt")

if not files:
    print("No files found in", TEXT_FILES_DIR)
    exit()

detailed_stats = []

print("="*60)
print("          Text File Sentiment Analysis Pipeline (XML-RPC)")
print("="*60)

total_start = time.time()

for filepath in files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r') as f:
        raw_text = f.read()

    print(f"\n📄 Processing file: {filename}")
    print("-"*60)

    start_file = time.time()

    # --- Clean Service ---
    proxy_clean = xmlrpc.client.ServerProxy(CLEAN_SERVICE_ADDR)
    proxy_clean.Process(raw_text, filename)

    # --- Wait until Report Service logs the result (ack) ---
    # Simple polling method
    proxy_report = xmlrpc.client.ServerProxy(REPORT_SERVICE_ADDR)
    report_done = False
    while not report_done:
        try:
            with open(os.path.join("reports", "results.csv"), "r") as f:
                lines = f.read().splitlines()
                # Check if current filename already logged
                if any(filename in line for line in lines):
                    report_done = True
        except FileNotFoundError:
            pass

    end_file = time.time()
    elapsed = end_file - start_file
    detailed_stats.append((filename, elapsed))
    print(f"✅ File processed in {elapsed:.4f}s")

total_end = time.time()
total_execution = total_end - total_start

# --- Detailed Summary Table ---
print("\n" + "="*60)
print("                  Detailed Processing Summary")
print("="*60)
print(f"{'File':<25} | {'Time (s)':<10} | {'Throughput (files/sec)':<20}")
print("-"*60)

for filepath, elapsed in detailed_stats:
    throughput = 1 / elapsed if elapsed > 0 else 0
    print(f"{filepath:<25} | {elapsed:<10.4f} | {throughput:<20.2f}")

avg_throughput = len(files)/total_execution if total_execution > 0 else 0
print("-"*60)
print(f"Total files processed: {len(files)}")
print(f"Total execution time: {total_execution:.4f}s")
print(f"Average throughput: {avg_throughput:.2f} files/sec")
print("="*60)
