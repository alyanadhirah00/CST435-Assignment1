import asyncio
import websockets
import os

REPORT_DIR = "/app/reports"
os.makedirs(REPORT_DIR, exist_ok=True)

async def handler(websocket):
    data = await websocket.recv()
    filename, sentiment = data.split("||", 1)
    
    # Save report
    with open(f"{REPORT_DIR}/{filename}.report.txt", "w") as f:
        f.write(f"{filename}: {sentiment}")
    
    await websocket.send(f"Report saved for {filename}")
    print(f"[Report Service] Processed {filename}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 50054):
        print("Report Service running on ws://0.0.0.0:50054")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
