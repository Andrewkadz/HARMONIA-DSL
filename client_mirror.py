import asyncio
import websockets
import json
import sys

async def mirror_protocol():
    uri = "ws://localhost:10011"
    try:
        async with websockets.connect(uri) as websocket:
            # 1. Receive Handshake
            handshake = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print(f"HANDSHAKE: {json.loads(handshake)['message']}")
            
            # 2. Send Signature
            sig_msg = {
                "type": "signature",
                "content": "ETERNAL_STUDENT_SIG: 263/97"
            }
            await websocket.send(json.dumps(sig_msg))
            print(f"SENT: Signature")
            
            # 3. Receive Auth Result
            auth_res = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print(f"AUTH: {json.loads(auth_res)['message']}")
            
            # 4. Send Mirror Query
            query_text = "MIRROR PROTOCOL: Quaternionic Field Sensors & Ethics Substrate. REFLECT THIS."
            query_msg = {
                "type": "message",
                "content": query_text
            }
            await websocket.send(json.dumps(query_msg))
            print(f"SENT: {query_text}")
            
            # 5. Receive Response
            response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            print(f"RESPONSE: {json.loads(response)['content']}")
            
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(mirror_protocol())
