import asyncio
import websockets
import json

REPORT_URI = "ws://localhost:50054"

# Simple lexicon
LEXICON = {"love": 2, "great": 2, "good": 1, "awesome": 3, "excellent": 3, "nice": 1, "best": 2,
    "hate": -2, "bad": -1, "terrible": -3, "awful": -3, "worst": -2, "poor": -1}

def sentiment_score(tokens):
    score = sum(LEXICON.get(token, 0) for token in tokens)
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

async def send_to_report(result, filename):
    async with websockets.connect(REPORT_URI) as websocket:
        await websocket.send(json.dumps({"result": result, "filename": filename}))
        print("Sent to Report Service:", result)

async def handler(websocket, path):
    data = await websocket.recv()
    data = json.loads(data)
    
    tokens = data["tokens"]
    filename = data["filename"]
    
    result = sentiment_score(tokens)
    await send_to_report(result, filename)
    await websocket.send("Sentiment analyzed and sent to Report Service")

async def main():
    async with websockets.serve(handler, "localhost", 50053):
        print("Sentiment Service running on ws://localhost:50053")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
