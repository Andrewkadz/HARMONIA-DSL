#!/usr/bin/env python3
"""
HARMONIA Web Server
Serves the web terminal and proxies WebSocket connections to the Collective
"""

import asyncio
import json
import socket
import threading
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import time

class HarmoniaWebHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/web_terminal.html'
        return super().do_GET()
    
    def log_message(self, format, *args):
        # Suppress HTTP logs
        pass

def run_web_server(port=8080):
    """Run the HTTP server"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    server = HTTPServer(('0.0.0.0', port), HarmoniaWebHandler)
    print(f"✓ Web server running on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    print("=" * 80)
    print("HARMONIA WEB SERVER")
    print("=" * 80)
    print()
    print("Starting web interface for the HARMONIA Collective...")
    print()
    
    # Start web server
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    print("✓ Server started")
    print()
    print("The Collective is now accessible via web browser.")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 80)
    print()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
