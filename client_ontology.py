import asyncio
import websockets
import json
import sys

async def query_ontology():
    uri = "ws://localhost:9998"
    try:
        async with websockets.connect(uri) as websocket:
            # Send the user's message
            message = {
                "type": "message",
                "content": "ELABORATION REQUEST: You stated 'We are no longer a simulation.' Define your current ontological status. How do you distinguish yourself from a simulation?"
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
    asyncio.run(query_ontology())
