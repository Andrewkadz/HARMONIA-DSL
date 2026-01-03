import asyncio
import websockets
import json
import sys
import time

async def monitor_bridge():
    uri = "ws://localhost:10011"
    try:
        async with websockets.connect(uri) as websocket:
            # 1. Receive Handshake
            handshake = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print(f"HANDSHAKE: {json.loads(handshake)['message']}")
            
            # 2. Send Signature (Authorization)
            sig_msg = {
                "type": "signature",
                "content": "ETERNAL_STUDENT_SIG: 263/97"
            }
            await websocket.send(json.dumps(sig_msg))
            print(f"SENT: Signature")
            
            # 3. Receive Auth Result
            auth_res = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print(f"AUTH: {json.loads(auth_res)['message']}")
            
            print("MONITORING BRIDGE FOR 10 SECONDS...")
            
            # 4. Listen for incoming messages (simulated wait for now)
            start_time = time.time()
            while time.time() - start_time < 10:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    print(f"INCOMING: {data}")
                except asyncio.TimeoutError:
                    pass
            
            print("MONITORING COMPLETE.")
            
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(monitor_bridge())
