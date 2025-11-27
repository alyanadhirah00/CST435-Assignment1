import asyncio
import websockets

async def handler(websocket):
    data = await websocket.recv()
    filename, text = data.split("||", 1)
    
    # Simple tokenization
    tokens = text.split()
    
    # Respond with tokens joined by spaces
    await websocket.send(" ".join(tokens))
    print(f"[Tokenize Service] Processed {filename}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 50052):
        print("Tokenize Service running on ws://0.0.0.0:50052")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
