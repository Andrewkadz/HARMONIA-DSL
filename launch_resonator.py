import sys
import os
import asyncio
import threading
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from harmonia_server import HarmoniaServer

def main():
    print("==========================================")
    print("PROJECT RESONATOR: PHASE 1 (NEURAL LINK)")
    print("==========================================")
    print("Initializing System...")
    
    # Initialize Server
    server = HarmoniaServer()
    server.initialize()
    
    print("✓ Core System Online")
    print("✓ Resonator Bridge Active")
    print("✓ Neural Voice Bridge Active")
    print("")
    print("Starting Real-Time Loop...")
    print("Listening on ws://0.0.0.0:9998")
    print("Press Ctrl+C to abort.")
    
    # Run Server
    try:
        server.run()
    except KeyboardInterrupt:
        print("\nShutting down Resonator...")

if __name__ == "__main__":
    main()
