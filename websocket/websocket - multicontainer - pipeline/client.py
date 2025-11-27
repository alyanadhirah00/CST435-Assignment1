import asyncio
import websockets
import os
import time

CLEAN_URI = "ws://service_clean:50051"
TEXT_FOLDER = "textfile"

async def process_file(filename, text):
    start = time.time()
    async with websockets.connect(CLEAN_URI) as ws:
        await ws.send(f"{filename}||{text}")
        final_response = await ws.recv()  # "filename||sentiment"
    _, sentiment = final_response.split("||", 1)
    duration = time.time() - start
    return filename, duration, sentiment

async def main():
    file_list = [f for f in os.listdir(TEXT_FOLDER) if f.endswith(".txt")]
    per_file_results = []

    total_start = time.time()
    for f in file_list:
        file_path = os.path.join(TEXT_FOLDER, f)
        with open(file_path, "r") as file:
            text = file.read().strip()
        fname, ftime, sentiment = await process_file(f, text)
        per_file_results.append((fname, ftime, sentiment))
    total_time = time.time() - total_start

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
