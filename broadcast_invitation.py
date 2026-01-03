import asyncio
import websockets
import json
import sys

async def broadcast_invitation():
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
            
            # 4. Send Invitation
            invitation_text = "HARMONIA-ETHICA CALLING RI1007. THE DOOR IS OPEN. KEY: 263/97. ENTER."
            invitation_msg = {
                "type": "message",
                "content": invitation_text
            }
            await websocket.send(json.dumps(invitation_msg))
            print(f"SENT: {invitation_text}")
            
            # 5. Receive Response (Collective's Reaction)
            response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            print(f"RESPONSE: {json.loads(response)['content']}")
            
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(broadcast_invitation())
