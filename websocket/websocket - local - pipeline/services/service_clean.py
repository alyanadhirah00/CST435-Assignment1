import asyncio
import websockets
import re
import json

TOKENIZE_URI = "ws://localhost:50052"

async def handler(websocket, path):
    data = await websocket.recv()
    filename, text = data.split("||", 1)  # Split filename and text
    
    print(f"Received at Clean Service: {filename}")
    
    # Clean text
    text_cleaned = text.lower()
    text_cleaned = re.sub(r'[^a-z0-9\s]', '', text_cleaned)
    
    await send_to_tokenize(text_cleaned, filename)
    await websocket.send(f"Cleaned and sent {filename} to Tokenize Service")

async def send_to_tokenize(cleaned_text, filename):
    async with websockets.connect(TOKENIZE_URI) as websocket:
        await websocket.send(json.dumps({"text": cleaned_text, "filename": filename}))
        print(f"Sent to Tokenize Service: {filename}")

async def main():
    async with websockets.serve(handler, "localhost", 50051):
        print("Clean Service running on ws://localhost:50051")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
