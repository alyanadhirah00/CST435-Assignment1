import asyncio
import websockets
import os
import time

CLEAN_URI = "ws://localhost:50051"
TEXT_FOLDER = "textfile"

async def send_file_sequential(filename, text):
    start_time = time.time()  # Start timing per file
    async with websockets.connect(CLEAN_URI) as websocket:
        await websocket.send(f"{filename}||{text}")
        response = await websocket.recv()
    end_time = time.time()
    file_time = end_time - start_time
    print(f"Processed {filename}: {response} (Time: {file_time:.4f}s)")
    return filename, file_time

async def main():
    file_list = [f for f in os.listdir(TEXT_FOLDER) if f.endswith(".txt")]
    per_file_times = []

    total_start = time.time()  # Start total timer

    # Sequential processing
    for filename in file_list:
        file_path = os.path.join(TEXT_FOLDER, filename)
        with open(file_path, 'r') as f:
            text = f.read().strip()
        fname, ftime = await send_file_sequential(filename, text)
        per_file_times.append((fname, ftime))

    total_end = time.time()
    total_time = total_end - total_start

    # Compute throughput per file and average throughput
    print("\n=== Detailed Processing Summary (Local Pipeline) ===")
    for fname, ftime in per_file_times:
        throughput = 1 / ftime if ftime > 0 else 0
        print(f"File: {fname} | Time: {ftime:.4f}s | Throughput: {throughput:.2f} files/sec")

    avg_throughput = len(per_file_times) / total_time if total_time > 0 else 0
    print(f"\nTotal files processed: {len(per_file_times)}")
    print(f"Total execution time: {total_time:.4f}s")
    print(f"Average throughput: {avg_throughput:.2f} files/sec")

if __name__ == "__main__":
    asyncio.run(main())
