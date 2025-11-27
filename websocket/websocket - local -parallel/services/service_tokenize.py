import asyncio
import websockets
import json

SENTIMENT_URI = "ws://localhost:50053"

async def send_to_sentiment(tokens, filename):
    async with websockets.connect(SENTIMENT_URI) as websocket:
        await websocket.send(json.dumps({"tokens": tokens, "filename": filename}))
        print("Sent to Sentiment Service:", tokens)

async def handler(websocket, path):
    data = await websocket.recv()
    data = json.loads(data)
    
    tokens = data["text"].split()
    filename = data["filename"]
    
    await send_to_sentiment(tokens, filename)
    await websocket.send("Tokenized and sent to Sentiment Service")

async def main():
    async with websockets.serve(handler, "localhost", 50052):
        print("Tokenize Service running on ws://localhost:50052")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
