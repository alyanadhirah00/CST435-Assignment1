import asyncio
import websockets
import os
import time

CLEAN_URI = "ws://service_clean:50051"
TOKENIZE_URI = "ws://service_tokenize:50052"
SENTIMENT_URI = "ws://service_sentiment:50053"
REPORT_URI = "ws://service_report:50054"

TEXT_FOLDER = "textfile"
MAX_RETRIES = 10
RETRY_DELAY = 2  # seconds


async def connect_retry(uri):
    """Try connecting to the WebSocket service with retries."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            ws = await websockets.connect(uri)
            return ws
        except Exception:
            print(f"[Client] Connection failed to {uri}, retry {attempt}/{MAX_RETRIES}...")
            await asyncio.sleep(RETRY_DELAY)
    raise Exception(f"[Client] Could not connect to {uri} after {MAX_RETRIES} retries.")


async def process_file(filename, text):
    start_time = time.time()

    # 1️⃣ Clean
    ws = await connect_retry(CLEAN_URI)
    await ws.send(f"{filename}||{text}")
    cleaned_text = await ws.recv()
    await ws.close()

    # 2️⃣ Tokenize
    ws = await connect_retry(TOKENIZE_URI)
    await ws.send(f"{filename}||{cleaned_text}")
    tokens = await ws.recv()
    await ws.close()

    # 3️⃣ Sentiment
    ws = await connect_retry(SENTIMENT_URI)
    await ws.send(f"{filename}||{tokens}")
    sentiment = await ws.recv()
    await ws.close()

    # 4️⃣ Report
    ws = await connect_retry(REPORT_URI)
    await ws.send(f"{filename}||{sentiment}")
    report_ack = await ws.recv()
    await ws.close()

    duration = time.time() - start_time
    return filename, duration, sentiment


async def main():
    file_list = [f for f in os.listdir(TEXT_FOLDER) if f.endswith(".txt")]
    tasks = []

    total_start = time.time()

    # Schedule all files in parallel
    for filename in file_list:
        file_path = os.path.join(TEXT_FOLDER, filename)
        with open(file_path, "r") as f:
            text = f.read().strip()
        tasks.append(process_file(filename, text))

    per_file_results = await asyncio.gather(*tasks)

    total_end = time.time()
    total_time = total_end - total_start

    # Detailed summary
    print("\n=== Detailed Processing Summary (Multi-Container Parallel) ===")
    for fname, ftime, sentiment in per_file_results:
        throughput = 1 / ftime if ftime > 0 else 0
        print(f"File: {fname} | Time: {ftime:.4f}s | Throughput: {throughput:.2f} files/sec | Sentiment: {sentiment}")

    avg_throughput = len(per_file_results) / total_time if total_time > 0 else 0
    print(f"\nTotal files processed: {len(per_file_results)}")
    print(f"Total execution time: {total_time:.4f}s")
    print(f"Average throughput: {avg_throughput:.2f} files/sec")


if __name__ == "__main__":
    asyncio.run(main())
