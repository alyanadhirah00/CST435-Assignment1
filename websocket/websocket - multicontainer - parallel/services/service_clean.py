import asyncio
import websockets
import re

async def handler(websocket, path):
    data = await websocket.recv()
    filename, text = data.split("||", 1)
    print(f"Clean received: {filename}")

    text_cleaned = text.lower()
    text_cleaned = re.sub(r'[^a-z0-9\s]', '', text_cleaned)

    await websocket.send(text_cleaned)  # respond back to client

async def main():
    async with websockets.serve(handler, "0.0.0.0", 50051):  # bind to 0.0.0.0
        print("Clean Service running on ws://0.0.0.0:50051")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
