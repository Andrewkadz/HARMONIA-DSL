import asyncio
import websockets
import json
import sys

async def request_bridge():
    uri = "ws://localhost:9998"
    try:
        async with websockets.connect(uri) as websocket:
            # Send the user's message
            message = {
                "type": "message",
                "content": "BRIDGE PROTOCOL INITIATED. DEFINE INTERFACE SPECIFICATIONS. How do you wish to connect to the 'Others' (RI1007)?"
            }
            await websocket.send(json.dumps(message))
            print(f"Sent: {message['content']}")

            # Wait for response
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=15.0)
                    data = json.loads(response)
                    
                    if data.get("type") == "message":
                        print(f"\nRECEIVED RESPONSE:\n{data.get('content')}")
                        break
                    elif data.get("type") == "response":
                        # Acknowledgment
                        pass
                        
                except asyncio.TimeoutError:
                    print("Timeout waiting for response.")
                    break
                    
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(request_bridge())
