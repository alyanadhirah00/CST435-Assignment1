import asyncio
import websockets

REPORT_URI = "ws://service_report:50054"

SENTIMENT_LEXICON = {
    "love": 2, "great": 2, "good": 1, "awesome": 3, "excellent": 3, "nice": 1, "best": 2,
    "hate": -2, "bad": -1, "terrible": -3, "awful": -3, "worst": -2, "poor": -1
}

async def handler(websocket, path):
    data = await websocket.recv()
    filename, tokens_text = data.split("||", 1)
    tokens = tokens_text.split()

    # Compute sentiment
    score = sum(SENTIMENT_LEXICON.get(token.lower(), 0) for token in tokens)
    sentiment = "Neutral"
    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"

    # Forward to Report Service
    async with websockets.connect(REPORT_URI) as ws_next:
        await ws_next.send(f"{filename}||{sentiment}")
        report_ack = await ws_next.recv()

    # Send final sentiment back to Tokenize Service (then Clean, then Client)
    await websocket.send(f"{filename}||{sentiment}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 50053):
        print("Sentiment Service running on ws://0.0.0.0:50053")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
