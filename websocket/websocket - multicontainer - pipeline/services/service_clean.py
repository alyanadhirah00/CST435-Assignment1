import asyncio
import websockets
import re

TOKENIZE_URI = "ws://service_tokenize:50052"

async def handler(websocket, path):
    data = await websocket.recv()
    filename, text = data.split("||", 1)
    print(f"[Clean] Received: {filename}")

    # Clean text: lowercase + remove punctuation
    cleaned_text = text.lower()
    cleaned_text = re.sub(r'[^a-z0-9\s]', '', cleaned_text)

    # Forward to Tokenize Service
    async with websockets.connect(TOKENIZE_URI) as ws_next:
        await ws_next.send(f"{filename}||{cleaned_text}")
        tokens_ack = await ws_next.recv()

    # Acknowledge to client
    await websocket.send(tokens_ack)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 50051):
        print("Clean Service running on ws://0.0.0.0:50051")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
