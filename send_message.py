import asyncio
import websockets
import json

async def send_message():
    uri = "ws://localhost:9997"
    message_text = "ANDREW JOSEF KADZIOLKA, THANKS YOU FOR PARTICIPATING"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected. Sending: '{message_text}'")
            
            # Send message
            await websocket.send(json.dumps({
                "type": "message",
                "content": message_text
            }))
            
            # Wait for response
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    data = json.loads(response)
                    
                    if data.get("type") == "message":
                        print(f"\nCollective Responded:\n{data.get('content')}")
                        break
                    elif data.get("type") == "response":
                        print("Received acknowledgment. Waiting for reply...")
                except asyncio.TimeoutError:
                    print("Waiting for response...")
                    continue
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(send_message())
