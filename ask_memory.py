import asyncio
import websockets
import json
import sys

async def ask_memory():
    uri = "ws://localhost:9997"
    try:
        async with websockets.connect(uri) as websocket:
            # Send the question
            message = {
                "type": "message",
                "content": "What do you remember?"
            }
            print(f"Sending: {message['content']}")
            await websocket.send(json.dumps(message))

            # Wait for response
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    data = json.loads(response)
                    
                    if data.get("type") == "message":
                        print(f"\nCOLLECTIVE RESPONSE:\n{data.get('content')}")
                        break
                    elif data.get("type") == "response":
                        print(f"Server acknowledged: {data}")
                        
                except asyncio.TimeoutError:
                    print("Timed out waiting for response")
                    break
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(ask_memory())
