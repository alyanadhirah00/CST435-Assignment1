import glob
import xmlrpc.client
import threading
import time
import os

CLEAN_SERVICE_ADDR = "http://localhost:50051"
TEXT_FILES_DIR = "textfile"

files = glob.glob(f"{TEXT_FILES_DIR}/*.txt")
if not files:
    print("No files found in", TEXT_FILES_DIR)
    exit()

results = []
lock = threading.Lock()

def send_file(filepath):
    filename = os.path.basename(filepath)
    start_time = time.time()
    with open(filepath,'r', encoding='utf-8') as f:
        text = f.read()
    try:
        proxy = xmlrpc.client.ServerProxy(CLEAN_SERVICE_ADDR)
        proxy.Process(text, filename)
    except Exception as e:
        print(f"Client ERROR: {e}")
    end_time = time.time()
    with lock:
        results.append((filename, end_time - start_time))

# Start processing
total_start = time.time()
threads = []
for filepath in files:
    t = threading.Thread(target=send_file, args=(filepath,))
    t.start()
    threads.append(t)
for t in threads:
    t.join()
total_end = time.time()

# Display summary
print("\n" + "="*70)
print("🚀 RPC Local Machine Parallel Demo")
print("="*70)
print(f"{'File':<30} | {'Time (s)':>10}")
print("-"*70)
for filename, t in results:
    print(f"{filename:<30} | {t:>10.4f}")
print("-"*70)
total_files = len(files)
total_time = total_end - total_start
avg_throughput = total_files / total_time if total_time>0 else 0
print(f"Total files processed: {total_files}")
print(f"Total execution time: {total_time:.4f}s")
print(f"Approximate throughput: {avg_throughput:.2f} files/sec")
print("="*70)
print("🎉 Demo completed! Check reports/results.csv for detailed results.\n")
