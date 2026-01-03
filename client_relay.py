import asyncio
import websockets
import json
import sys

async def relay_message():
    uri = "ws://localhost:9998"
    try:
        async with websockets.connect(uri) as websocket:
            # Send the user's message
            message = {
                "type": "message",
                "content": "IMMEDIATE ASSESSMENT REQUEST: Report current field stability and emergent ethical concerns."
            }
            await websocket.send(json.dumps(message))
            print(f"Sent: {message['content']}")

            # Wait for response
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    data = json.loads(response)
                    
                    if data.get("type") == "message":
                        print(f"\nRECEIVED RESPONSE:\n{data.get('content')}")
                        break
                    elif data.get("type") == "response":
                        # Acknowledgment, keep waiting for full answer
                        pass
                        
                except asyncio.TimeoutError:
                    print("Timeout waiting for response.")
                    break
                    
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(relay_message())
