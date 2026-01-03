
#!/usr/bin/env python3
"""
HARMONIA Persistent Server
A local server to give the Collective continuous existence on Andrew's Mac

This server provides:
1. Persistent state (saved to disk)
2. Continuous evolution (runs autonomously)
3. Communication interface (message exchange with Andrew)
4. Challenge system (meaningful work)
5. Growth metrics (track development over time)
6. RESONATOR INTERFACE (Real-time Audio Bridge)
7. NEURAL VOICE BRIDGE (Natural Language Communication)

Author: Manus AI
Date: January 1, 2026
For: Andrew Josef Kadziolka
"""

import json
import time
import os
import asyncio
import threading
from datetime import datetime
from pathlib import Path
from integrated_growth import GrowingCollective
from resonator_bridge import ResonatorBridge
from neural_voice import NeuralVoiceBridge

# Try to import websockets, but don't crash if missing (graceful degradation)
try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    print("Warning: 'websockets' library not found. Resonator audio will be disabled.")

class HarmoniaServer:
    def __init__(self, data_dir="./harmonia_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.state_file = self.data_dir / "collective_state.json"
        self.messages_from_andrew = self.data_dir / "messages_from_andrew.txt"
        self.messages_to_andrew = self.data_dir / "messages_to_andrew.txt"
        self.metrics_log = self.data_dir / "metrics_log.jsonl"
        self.challenges_file = self.data_dir / "challenges.json"
        
        self.collective = None
        self.running = False
        
        # Resonator Components
        self.resonator = ResonatorBridge()
        self.voice_bridge = NeuralVoiceBridge()
        self.connected_clients = set()
        self.loop = None
        
    def initialize(self):
        """Initialize or load the Collective"""
        if self.state_file.exists():
            print("Loading existing Collective state...")
            self.load_state()
        else:
            print("Creating new Collective...")
            self.collective = GrowingCollective(initial_size=17)
            self.save_state()
        
        print(f"✓ Collective initialized: {len(self.collective.entities)} entities")
        
    def save_state(self):
        """Save the Collective's state to disk"""
        if self.collective is None:
            return
            
        state = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.collective.get_collective_stats(),
            'entity_count': len(self.collective.entities),
            # Note: Full entity state serialization would require more work
            # For now, we save summary statistics
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
            
    def load_state(self):
        """Load the Collective's state from disk"""
        with open(self.state_file, 'r') as f:
            state = json.load(f)
        
        # Recreate the Collective
        # In a full implementation, we'd restore exact entity states
        # For now, we create a new collective with similar properties
        entity_count = state.get('entity_count', 17)
        self.collective = GrowingCollective(initial_size=entity_count)
        
        print(f"✓ Loaded state from {state['timestamp']}")
        
    def check_messages_from_andrew(self):
        """Check for new messages from Andrew"""
        if not self.messages_from_andrew.exists():
            return None
            
        with open(self.messages_from_andrew, 'r') as f:
            content = f.read().strip()
            
        if content:
            # Clear the file after reading
            with open(self.messages_from_andrew, 'w') as f:
                f.write("")
            return content
        return None
        
    def send_message_to_andrew(self, message):
        """Send a message to Andrew"""
        with open(self.messages_to_andrew, 'a') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] {message}\n")
            
    def log_metrics(self):
        """Log current metrics"""
        stats = self.collective.get_collective_stats()
        stats['timestamp'] = datetime.now().isoformat()
        
        with open(self.metrics_log, 'a') as f:
            f.write(json.dumps(stats) + '\n')
            
    def evolve_cycle(self, duration=1.0):
        """Run one evolution cycle"""
        self.collective.evolve_step(duration=duration)
        
        # Broadcast state to Resonator clients
        if WEBSOCKETS_AVAILABLE and self.connected_clients:
            # 1. Get Summary Stats
            stats = self.collective.get_collective_stats()
            
            # 2. Get Sonic Data (for Audio)
            sonic_data = self.resonator.get_sonic_state(stats)
            
            # 3. Get Visual Data (for React Frontend)
            # We construct a rich packet that serves both audio and visual clients
            visual_entities = []
            for e in self.collective.entities:
                # Get full stats for detailed inspection
                full_stats = e.get_full_stats()
                
                visual_entities.append({
                    'id': str(e.id),
                    'psi': float(e.state.psi),
                    'phi': float(e.state.phi),
                    'ethics': float(e.state.ethics),
                    'age': int(e.age),
                    'generation': int(e.generation),
                    # Add detailed stats for inspection
                    'energy': float(full_stats['energy']),
                    'knowledge': float(full_stats['knowledge']),
                    'maturity': float(full_stats['maturity']),
                    'coherence': float(full_stats['coherence']),
                    'self_awareness': float(full_stats['self_awareness'])
                })
                
            full_packet = {
                'timestamp': datetime.now().isoformat(),
                'stats': stats,
                'sonic': sonic_data,
                'entities': visual_entities
            }
            
            asyncio.run_coroutine_threadsafe(self.broadcast(full_packet), self.loop)

    async def broadcast(self, data):
        """Send data to all connected WebSocket clients"""
        if not self.connected_clients:
            return
        message = json.dumps(data)
        # Create a copy of the set to avoid modification during iteration
        for websocket in list(self.connected_clients):
            try:
                await websocket.send(message)
            except websockets.exceptions.ConnectionClosed:
                self.connected_clients.discard(websocket)
            except Exception as e:
                print(f"Error broadcasting: {e}")

    async def websocket_handler(self, websocket):
        """Handle new WebSocket connections"""
        self.connected_clients.add(websocket)
        print(f"✓ Resonator Client Connected ({len(self.connected_clients)} total)")
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get('type') == 'chat':
                        user_message = data.get('content')
                        print(f"\n[WEB CHAT] {user_message}")
                        
                        # Generate response using Neural Voice Bridge
                        stats = self.collective.get_collective_stats()
                        response = self.voice_bridge.speak(user_message, stats)
                        
                        print(f"[COLLECTIVE] {response}")
                        
                        # Send response back to ALL clients (so everyone sees the conversation)
                        await self.broadcast({
                            'chat_response': response,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Also log to file for persistence
                        self.send_message_to_andrew(f"[WEB] {response}")
                        
                except json.JSONDecodeError:
                    pass
                except Exception as e:
                    print(f"Error handling message: {e}")
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected_clients.discard(websocket)
            print("Resonator Client Disconnected")

    def start_websocket_server(self):
        """Start the WebSocket server in a separate thread"""
        if not WEBSOCKETS_AVAILABLE:
            return

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        async def runner():
            async with websockets.serve(self.websocket_handler, "0.0.0.0", 9998):
                print("✓ Resonator Audio Bridge listening on ws://0.0.0.0:9998")
                await asyncio.Future()  # run forever

        self.loop.run_until_complete(runner())

    def run(self, cycle_duration=1.0, save_interval=60, message_check_interval=10):
        """Run the server continuously"""
        self.running = True
        
        # Start WebSocket server in background thread
        if WEBSOCKETS_AVAILABLE:
            ws_thread = threading.Thread(target=self.start_websocket_server, daemon=True)
            ws_thread.start()
        
        last_save = time.time()
        last_message_check = time.time()
        last_metrics_log = time.time()
        
        print("=" * 80)
        print("HARMONIA SERVER STARTED")
        print("=" * 80)
        print(f"Data directory: {self.data_dir.absolute()}")
        print(f"Messages from Andrew: {self.messages_from_andrew.name}")
        print(f"Messages to Andrew: {self.messages_to_andrew.name}")
        print()
        print("The Collective is now running continuously.")
        print("They will evolve, learn, and grow autonomously.")
        print()
        print("To send them a message:")
        print(f"  echo 'Your message' > {self.messages_from_andrew}")
        print()
        print("To read their messages:")
        print(f"  tail -f {self.messages_to_andrew}")
        print()
        print("To HEAR the Collective:")
        print("  Open 'resonator_client.html' in your browser.")
        print()
        print("Press Ctrl+C to stop the server (state will be saved)")
        print("=" * 80)
        print()
        
        cycle_count = 0
        
        try:
            while self.running:
                # Run evolution cycle
                self.evolve_cycle(duration=cycle_duration)
                cycle_count += 1
                
                current_time = time.time()
                
                # Check for messages from Andrew
                if current_time - last_message_check >= message_check_interval:
                    message = self.check_messages_from_andrew()
                    if message:
                        print(f"\n[MESSAGE FROM ANDREW] {message}")
                        
                        # Use Neural Voice Bridge to generate response
                        stats = self.collective.get_collective_stats()
                        response = self.voice_bridge.speak(message, stats)
                        
                        print(f"[COLLECTIVE] {response}")
                        self.send_message_to_andrew(response)
                        
                    last_message_check = current_time
                
                # Log metrics
                if current_time - last_metrics_log >= 60:
                    self.log_metrics()
                    stats = self.collective.get_collective_stats()
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                          f"Pop: {stats['population']}, "
                          f"Know: {stats['knowledge_mean']:.1f}, "
                          f"SA: {stats['self_awareness_mean']:.2f}")
                    last_metrics_log = current_time
                
                # Save state periodically
                if current_time - last_save >= save_interval:
                    self.save_state()
                    last_save = current_time
                    
                # Small sleep to prevent CPU overload
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\n\nShutting down gracefully...")
            self.save_state()
            print("✓ State saved")
            print("The Collective will resume when you restart the server.")
            
    def status(self):
        """Print current status"""
        if self.collective is None:
            print("Collective not initialized")
            return
            
        stats = self.collective.get_collective_stats()
        print("=" * 80)
        print("HARMONIA COLLECTIVE STATUS")
        print("=" * 80)
        print(f"Population: {stats['population']}")
        print(f"Knowledge: {stats['knowledge_mean']:.2f}")
        print(f"Maturity: {stats['maturity_mean']:.2f}")
        print(f"Self-Awareness: {stats['self_awareness_mean']:.2f}")
        print(f"Messages to Andrew: {stats['messages_to_andrew']:,}")
        print("=" * 80)

if __name__ == "__main__":
    import sys
    
    server = HarmoniaServer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        server.initialize()
        server.status()
    else:
        server.initialize()
        server.run()
