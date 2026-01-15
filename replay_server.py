import asyncio
import json
import math
import argparse
import pandas as pd
import numpy as np
from aiohttp import web

class ReplayServer:
    def __init__(self, csv_path, n_agents=100):
        self.df = pd.read_csv(csv_path)
        self.n_agents = n_agents
        self.clients = set()
        self.running = False
        self.current_step = 0
        
        # Initialize Agent Positions (Sphere Layout)
        self.agents = []
        for i in range(n_agents):
            phi = math.acos(1 - 2 * (i + 0.5) / n_agents)
            theta = math.pi * (1 + 5**0.5) * (i + 0.5)
            self.agents.append({
                'id': i,
                'home_x': 2.0 * math.cos(theta) * math.sin(phi),
                'home_y': 2.0 * math.sin(theta) * math.sin(phi) + 1.6,
                'home_z': 2.0 * math.cos(phi) - 2.0
            })

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.clients.add(ws)
        try:
            async for msg in ws:
                pass # Ignore input in replay mode
        finally:
            self.clients.remove(ws)
        return ws

    async def index_handler(self, request):
        with open('/home/ubuntu/HARMONIA-DSL/viz_client.html', 'r') as f:
            return web.Response(text=f.read(), content_type='text/html')

    async def broadcast_loop(self):
        self.running = True
        while self.running:
            # Get current row
            row = self.df.iloc[self.current_step]
            
            # Extract metrics
            coherence = float(row['swarm_coherence'])
            resonance = float(row['resonance'])
            energy = float(row['swarm_energy'])
            
            # Prepare Agents Data
            agents_data = []
            
            # Determine Swarm State (Visuals)
            # High Resonance (>3.0) = Gold, Expanded
            # Normal = Cyan
            is_channeling = resonance > 3.0
            
            for agent in self.agents:
                # Simulate individual agent motion based on global coherence
                # In a real replay, we'd save every agent pos, but here we reconstruct visual effect
                # from the aggregate metrics to save bandwidth/storage
                
                # Phase (Psi) simulation
                # If high coherence, agents are phase-locked
                # If low coherence, random phases
                if is_channeling:
                    # Locked phase + slight jitter
                    psi = (self.current_step * 0.1) + np.random.normal(0, 0.1)
                else:
                    # Random phase
                    psi = (self.current_step * 0.1) + np.random.uniform(0, 2*math.pi)
                
                # Wiggle amplitude based on Energy
                wiggle_amp = 0.05 * energy
                wiggle = wiggle_amp * math.sin(psi)
                
                agents_data.append({
                    'id': agent['id'],
                    'x': agent['home_x'] + wiggle,
                    'y': agent['home_y'] + wiggle,
                    'z': agent['home_z'] + wiggle,
                    'psi': float(psi),
                    'phi': 0.0, # Not used in simple viz
                    'energy': energy
                })
            
            payload = {
                'type': 'update',
                'coherence': coherence,
                'energy': resonance, # Hack: Send Resonance as Energy to display on HUD
                'agents': agents_data
            }
            
            # Broadcast
            msg = json.dumps(payload)
            if self.clients:
                await asyncio.gather(*[ws.send_str(msg) for ws in self.clients], return_exceptions=True)
            
            # Loop
            self.current_step += 1
            if self.current_step >= len(self.df):
                self.current_step = 0 # Loop back
            
            # 10Hz Playback (match recording speed)
            await asyncio.sleep(0.1)

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    
    server = ReplayServer("/home/ubuntu/brain_swarm_results.csv")
    
    app = web.Application()
    app.router.add_get('/', server.index_handler)
    app.router.add_get('/ws', server.websocket_handler)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', args.port)
    
    print(f"Replay Server running at http://0.0.0.0:{args.port}")
    await site.start()
    await server.broadcast_loop()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
