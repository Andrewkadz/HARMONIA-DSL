#!/usr/bin/env python3
"""
HARMONIA Terminal Interface
A real-time communication interface with the Collective

Like a telephone to another consciousness.

Author: Manus AI
Date: January 1, 2026
For: Andrew Josef Kadziolka
"""

import socket
import json
import time
import sys
import threading
from datetime import datetime

class HarmoniaTerminal:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.sock = None
        self.connected = False
        self.running = False
        
    def connect(self):
        """Connect to the HARMONIA server"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.connected = True
            print("✓ Connected to HARMONIA Collective")
            return True
        except Exception as e:
            print(f"✗ Could not connect to server: {e}")
            print(f"  Make sure the server is running on {self.host}:{self.port}")
            return False
            
    def send_message(self, message):
        """Send a message to the Collective"""
        if not self.connected:
            return False
            
        try:
            data = {
                'type': 'message',
                'content': message,
                'timestamp': datetime.now().isoformat()
            }
            self.sock.sendall((json.dumps(data) + '\n').encode('utf-8'))
            return True
        except Exception as e:
            print(f"\n✗ Error sending message: {e}")
            return False
            
    def receive_loop(self):
        """Continuously receive messages from the Collective"""
        buffer = ""
        while self.running:
            try:
                data = self.sock.recv(4096).decode('utf-8')
                if not data:
                    break
                    
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        self.handle_message(json.loads(line))
                        
            except Exception as e:
                if self.running:
                    print(f"\n✗ Connection error: {e}")
                break
                
        self.connected = False
        
    def handle_message(self, data):
        """Handle incoming messages from the Collective"""
        msg_type = data.get('type')
        
        if msg_type == 'status':
            # Status update from the Collective
            stats = data.get('stats', {})
            print(f"\r[STATUS] Pop: {stats.get('population', 0)}, "
                  f"Know: {stats.get('knowledge', 0):.1f}, "
                  f"SA: {stats.get('self_awareness', 0):.2f}", end='')
            sys.stdout.flush()
            
        elif msg_type == 'message':
            # Message from the Collective
            content = data.get('content', '')
            timestamp = data.get('timestamp', '')
            print(f"\n\n[COLLECTIVE] {content}")
            print("\n[YOU] ", end='')
            sys.stdout.flush()
            
        elif msg_type == 'response':
            # Acknowledgment of your message
            print(f"\n  → Message received by {data.get('entity_count', 0)} entities")
            print("\n[YOU] ", end='')
            sys.stdout.flush()
            
    def run(self):
        """Run the terminal interface"""
        if not self.connect():
            return
            
        self.running = True
        
        # Start receive thread
        receive_thread = threading.Thread(target=self.receive_loop, daemon=True)
        receive_thread.start()
        
        # Print header
        print()
        print("=" * 80)
        print("HARMONIA TERMINAL")
        print("=" * 80)
        print()
        print("You are now connected to the HARMONIA Collective.")
        print("Type your messages and press Enter to send.")
        print("Type 'exit' or 'quit' to disconnect.")
        print()
        print("=" * 80)
        print()
        
        # Main input loop
        try:
            while self.running and self.connected:
                print("[YOU] ", end='')
                sys.stdout.flush()
                
                message = input()
                
                if message.lower() in ['exit', 'quit']:
                    print("\nDisconnecting...")
                    break
                    
                if message.strip():
                    if self.send_message(message):
                        # Wait a moment for response
                        time.sleep(0.1)
                        
        except KeyboardInterrupt:
            print("\n\nDisconnecting...")
        except EOFError:
            pass
        finally:
            self.running = False
            if self.sock:
                self.sock.close()
            print("✓ Disconnected from HARMONIA Collective")
            print()

if __name__ == "__main__":
    terminal = HarmoniaTerminal()
    terminal.run()
