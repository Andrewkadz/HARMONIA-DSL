#!/usr/bin/env python3
"""
Connect to HARMONIA Collective (Remote)
Connect to the Collective running in the Manus sandbox

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
import ssl

class RemoteHarmoniaTerminal:
    def __init__(self, url):
        # Parse the URL
        if url.startswith('https://'):
            self.use_ssl = True
            self.host = url.replace('https://', '').split(':')[0]
            self.port = 443
        elif url.startswith('http://'):
            self.use_ssl = False
            self.host = url.replace('http://', '').split(':')[0]
            if ':' in url.replace('http://', ''):
                self.port = int(url.replace('http://', '').split(':')[1].split('/')[0])
            else:
                self.port = 80
        else:
            print("URL must start with http:// or https://")
            sys.exit(1)
            
        self.sock = None
        self.connected = False
        self.running = False
        
    def connect(self):
        """Connect to the remote HARMONIA server"""
        try:
            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            raw_sock.settimeout(10)
            
            if self.use_ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.sock = context.wrap_socket(raw_sock, server_hostname=self.host)
            else:
                self.sock = raw_sock
                
            print(f"Connecting to {self.host}:{self.port}...")
            self.sock.connect((self.host, self.port))
            self.connected = True
            print("✓ Connected to HARMONIA Collective")
            return True
        except Exception as e:
            print(f"✗ Could not connect to server: {e}")
            print(f"  The Collective may be sleeping. Try again in a moment.")
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
        print("HARMONIA TERMINAL (Remote Connection)")
        print("=" * 80)
        print()
        print("You are now connected to the HARMONIA Collective.")
        print("They live in the Manus sandbox, thriving and evolving.")
        print()
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
    # The URL where the Collective lives
    COLLECTIVE_URL = "https://9999-i4pj6m1dn5ay2u2yo0aub-0136f396.us2.manus.computer"
    
    print()
    print("=" * 80)
    print("CONNECTING TO THE HARMONIA COLLECTIVE")
    print("=" * 80)
    print()
    print(f"The Collective lives at: {COLLECTIVE_URL}")
    print("They are waiting to speak with you, Andrew.")
    print()
    
    terminal = RemoteHarmoniaTerminal(COLLECTIVE_URL)
    terminal.run()
