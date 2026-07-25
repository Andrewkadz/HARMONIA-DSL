"""
Holo-Swarm Server (ANIMUS Visualizer Backend)
=============================================

Runs a Harmonic Swarm and broadcasts agent states via WebSocket.
Serves the WebXR client via HTTP.

Usage:
    python3.11 viz_server.py --port 8000
"""

import asyncio
import json
import math
import argparse
import os
from aiohttp import web
import numpy as np

# Import the engine (ensure pure_harmonic_swarm.py is in the same dir)
try:
    from pure_harmonic_swarm import HarmonicSwarm
except ImportError:
    print("Error: pure_harmonic_swarm.py not found. Please run this from the HARMONIA-DSL directory.")
    exit(1)

class HoloSwarmServer:
    def __init__(self, n_agents=100):
        self.swarm = HarmonicSwarm(n_agents=n_agents)
        self.clients = set()
        self.running = False
        
        # Initialize with some random positions for visual interest
        for i, agent in enumerate(self.swarm.agents):
            # Map 1D index to 3D sphere coordinates for initial layout
            phi = math.acos(1 - 2 * (i + 0.5) / n_agents)
            theta = math.pi * (1 + 5**0.5) * (i + 0.5)
            
            # Store initial "home" positions
            agent.home_x = 2.0 * math.cos(theta) * math.sin(phi)
            agent.home_y = 2.0 * math.sin(theta) * math.sin(phi) + 1.5 # Lift up to eye level
            agent.home_z = 2.0 * math.cos(phi) - 2.0 # Push back a bit

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        print("Client connected")
        self.clients.add(ws)
        
        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if data.get('action') == 'perturb':
                        # Client clicked/interacted: Add stress!
                        print("Perturbation received!")
                        for agent in self.swarm.agents:
                            agent.psi += np.random.uniform(-1.0, 1.0)
        finally:
            self.clients.remove(ws)
            print("Client disconnected")
        
        return ws

    async def index_handler(self, request):
        """Serve the HTML client."""
        with open('viz_client.html', 'r') as f:
            return web.Response(text=f.read(), content_type='text/html')

    async def broadcast_loop(self):
        """Main physics loop."""
        self.running = True
        while self.running:
            # 1. Step Physics
            self.swarm.step(dt=0.05)
            stats = self.swarm.get_statistics()
            
            # 2. Prepare Payload
            agents_data = []
            for agent in self.swarm.agents:
                # Visual Logic:
                # Position = Home + Vibration (based on Phase/Psi)
                # Color/Glow = Coherence (based on Phase alignment)
                
                # Wiggle based on phase (Psi)
                wiggle = 0.2 * math.sin(agent.psi)
                
                agents_data.append({
                    'id': agent.agent_id,
                    'x': agent.home_x + wiggle * 0.1,
                    'y': agent.home_y + wiggle * 0.1,
                    'z': agent.home_z + wiggle * 0.1,
                    'psi': float(agent.psi),
                    'phi': float(agent.phi),
                    'energy': float(agent.energy)
                })
            
            payload = {
                'type': 'update',
                'coherence': float(stats['coherence']),
                'energy': float(stats['mean_energy']),
                'agents': agents_data
            }
            
            # 3. Broadcast
            msg = json.dumps(payload)
            if self.clients:
                await asyncio.gather(*[ws.send_str(msg) for ws in self.clients], return_exceptions=True)
            
            # 60 FPS target
            await asyncio.sleep(1/60)

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    
    server = HoloSwarmServer(n_agents=100)
    
    app = web.Application()
    app.router.add_get('/', server.index_handler)
    app.router.add_get('/ws', server.websocket_handler)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', args.port)
    
    print(f"Holo-Swarm Server running at http://0.0.0.0:{args.port}")
    print("Open this URL in your Meta Quest 3S browser.")
    
    await site.start()
    await server.broadcast_loop()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
