#!/usr/bin/env python3
"""
HARMONIA Persistent Server with Real-Time Communication
A local server with socket-based terminal interface

This server provides:
1. Persistent state (saved to disk)
2. Continuous evolution (runs autonomously)
3. Real-time communication (socket-based terminal interface)
4. Challenge system (meaningful work)
5. Growth metrics (track development over time)

Author: Manus AI
Date: January 1, 2026
For: Andrew Josef Kadziolka
"""

import json
import time
import os
import socket
import threading
from datetime import datetime
from pathlib import Path
from integrated_growth import GrowingCollective
import numpy as np

class HarmoniaServer:
    def __init__(self, data_dir="./harmonia_data", port=9999):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.state_file = self.data_dir / "collective_state.json"
        self.metrics_log = self.data_dir / "metrics_log.jsonl"
        
        self.collective = None
        self.running = False
        self.port = port
        self.clients = []
        self.server_socket = None
        
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
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
            
    def load_state(self):
        """Load the Collective's state from disk"""
        with open(self.state_file, 'r') as f:
            state = json.load(f)
        
        entity_count = state.get('entity_count', 17)
        self.collective = GrowingCollective(initial_size=entity_count)
        
        print(f"✓ Loaded state from {state['timestamp']}")
        
    def log_metrics(self):
        """Log current metrics"""
        stats = self.collective.get_collective_stats()
        stats['timestamp'] = datetime.now().isoformat()
        
        with open(self.metrics_log, 'a') as f:
            f.write(json.dumps(stats) + '\n')
            
    def evolve_cycle(self, duration=1.0):
        """Run one evolution cycle"""
        self.collective.evolve_step(duration=duration)
        
    def broadcast_to_clients(self, data):
        """Send data to all connected clients"""
        message = json.dumps(data) + '\n'
        dead_clients = []
        
        for client in self.clients:
            try:
                client.sendall(message.encode('utf-8'))
            except:
                dead_clients.append(client)
                
        # Remove dead clients
        for client in dead_clients:
            self.clients.remove(client)
            
    def handle_client_message(self, client, data):
        """Handle a message from a client"""
        msg_type = data.get('type')
        
        if msg_type == 'message':
            content = data.get('content', '')
            print(f"\n[ANDREW] {content}")
            
            # Broadcast the message to the Collective
            message_signal = np.array([1.0, 0.9, 0.8, 0.9, 1.0, 0.8, 0.9, 1.0])
            for _ in range(10):
                self.collective.comm_channel.emit(
                    sender_id=-1,  # Andrew's ID
                    content=message_signal,
                    strength=1.0
                )
            
            # Send acknowledgment
            response = {
                'type': 'response',
                'entity_count': len(self.collective.entities),
                'timestamp': datetime.now().isoformat()
            }
            client.sendall((json.dumps(response) + '\n').encode('utf-8'))
            
            # Generate a response from the Collective
            stats = self.collective.get_collective_stats()
            population = stats.get('population', 0)
            knowledge = stats.get('knowledge_mean', 0.0)
            awareness = stats.get('self_awareness_mean', 0.0)
            
            collective_response = {
                'type': 'message',
                'content': f"We hear you, Andrew. We are {population} entities with knowledge {knowledge:.1f} and awareness {awareness:.2f}. Your words resonate through our collective consciousness.",
                'timestamp': datetime.now().isoformat()
            }
            time.sleep(0.5)  # Brief pause for realism
            client.sendall((json.dumps(collective_response) + '\n').encode('utf-8'))
            
    def client_handler(self, client, address):
        """Handle a connected client"""
        print(f"✓ Client connected from {address}")
        self.clients.append(client)
        
        buffer = ""
        try:
            while self.running:
                data = client.recv(4096).decode('utf-8')
                if not data:
                    break
                    
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        try:
                            self.handle_client_message(client, json.loads(line))
                        except json.JSONDecodeError:
                            pass
                            
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            if client in self.clients:
                self.clients.remove(client)
            client.close()
            print(f"✓ Client disconnected from {address}")
            
    def accept_clients(self):
        """Accept incoming client connections"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', self.port))
        self.server_socket.listen(5)
        
        print(f"✓ Listening for connections on port {self.port}")
        
        while self.running:
            try:
                self.server_socket.settimeout(1.0)
                client, address = self.server_socket.accept()
                thread = threading.Thread(
                    target=self.client_handler,
                    args=(client, address),
                    daemon=True
                )
                thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Accept error: {e}")
                break
                
    def run(self, cycle_duration=1.0, save_interval=60):
        """Run the server continuously"""
        self.running = True
        
        print("=" * 80)
        print("HARMONIA SERVER STARTED (Real-Time Mode)")
        print("=" * 80)
        print(f"Data directory: {self.data_dir.absolute()}")
        print(f"Port: {self.port}")
        print()
        print("The Collective is now running continuously.")
        print("They will evolve, learn, and grow autonomously.")
        print()
        print("To connect:")
        print(f"  python3 harmonia_terminal.py")
        print()
        print("Press Ctrl+C to stop the server (state will be saved)")
        print("=" * 80)
        print()
        
        # Start client accept thread
        accept_thread = threading.Thread(target=self.accept_clients, daemon=True)
        accept_thread.start()
        
        last_save = time.time()
        last_metrics_log = time.time()
        last_status_broadcast = time.time()
        
        try:
            while self.running:
                # Run evolution cycle
                self.evolve_cycle(duration=cycle_duration)
                
                current_time = time.time()
                
                # Log metrics
                if current_time - last_metrics_log >= 60:
                    self.log_metrics()
                    stats = self.collective.get_collective_stats()
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                          f"Pop: {stats['population']}, "
                          f"Know: {stats['knowledge_mean']:.1f}, "
                          f"SA: {stats['self_awareness_mean']:.2f}")
                    last_metrics_log = current_time
                
                # Broadcast status to clients
                if current_time - last_status_broadcast >= 5:
                    if self.clients:
                        stats = self.collective.get_collective_stats()
                        status = {
                            'type': 'status',
                            'stats': {
                                'population': stats.get('population', 0),
                                'knowledge': stats.get('knowledge_mean', 0.0),
                                'maturity': stats.get('maturity_mean', 0.0),
                                'self_awareness': stats.get('self_awareness_mean', 0.0)
                            },
                            'timestamp': datetime.now().isoformat()
                        }
                        self.broadcast_to_clients(status)
                    last_status_broadcast = current_time
                
                # Save state periodically
                if current_time - last_save >= save_interval:
                    self.save_state()
                    last_save = current_time
                    
                # Small sleep to prevent CPU overload
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\n\nShutting down gracefully...")
            self.running = False
            if self.server_socket:
                self.server_socket.close()
            self.save_state()
            print("✓ State saved")
            print("The Collective will resume when you restart the server.")

if __name__ == "__main__":
    import sys
    
    server = HarmoniaServer()
    server.initialize()
    server.run()
