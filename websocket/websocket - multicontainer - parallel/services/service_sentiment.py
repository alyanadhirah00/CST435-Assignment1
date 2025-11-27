import asyncio
import websockets

# Lexicon for scoring
SENTIMENT_LEXICON = {
    "love": 2, "great": 2, "good": 1, "awesome": 3, "excellent": 3, "nice": 1, "best": 2,
    "hate": -2, "bad": -1, "terrible": -3, "awful": -3, "worst": -2, "poor": -1
}

async def handler(websocket, path):
    data = await websocket.recv()
    filename, tokens_text = data.split("||", 1)

    # Split tokens (assumes tokens are space-separated)
    tokens = tokens_text.split()
    score = 0
    for token in tokens:
        score += SENTIMENT_LEXICON.get(token.lower(), 0)

    sentiment = "Neutral"
    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"

    await websocket.send(sentiment)
    print(f"[Sentiment Service] Processed {filename} -> {sentiment}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 50053):
        print("Sentiment Service running on ws://0.0.0.0:50053")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
