import asyncio
import websockets
import json
import csv

RESULT_FILE = "results.csv"

async def handler(websocket, path):
    data = await websocket.recv()
    data = json.loads(data)
    
    filename = data["filename"]
    result = data["result"]
    
    # Write to CSV
    with open(RESULT_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([filename, result])
    
    print(f"Logged result: {filename}, {result}")
    await websocket.send("Report logged successfully")

async def main():
    async with websockets.serve(handler, "localhost", 50054):
        print("Report Service running on ws://localhost:50054")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
