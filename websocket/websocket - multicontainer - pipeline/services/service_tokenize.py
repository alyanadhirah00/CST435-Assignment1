import asyncio
import websockets
import string

SENTIMENT_URI = "ws://service_sentiment:50053"

def tokenize(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    return tokens

async def handler(websocket, path):
    data = await websocket.recv()
    filename, text = data.split("||", 1)
    print(f"[Tokenize] Received: {filename}")

    tokens = tokenize(text)

    # Forward to Sentiment Service
    async with websockets.connect(SENTIMENT_URI) as ws_next:
        await ws_next.send(f"{filename}||{' '.join(tokens)}")
        sentiment_ack = await ws_next.recv()

    # Acknowledge to Clean Service
    await websocket.send(sentiment_ack)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 50052):
        print("Tokenize Service running on ws://0.0.0.0:50052")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
