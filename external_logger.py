import asyncio
import websockets
import json
import csv
from datetime import datetime
import time

async def log_evolution():
    uri = "ws://localhost:9997"
    log_file = "evolution_data_external.csv"
    
    # Write header
    with open(log_file, "w") as f:
        f.write("timestamp,population,knowledge,awareness,energy\n")
        
    print(f"Logging to {log_file}...")
    
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to Collective.")
                
                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        data = json.loads(message)
                        
                        if data.get("type") == "status":
                            stats = data.get("stats", {})
                            timestamp = datetime.now().isoformat()
                            
                            log_line = f"{timestamp},{stats.get('population')},{stats.get('knowledge')},{stats.get('awareness')},{stats.get('energy')}"
                            
                            with open(log_file, "a") as f:
                                f.write(log_line + "\n")
                                
                            print(f"Logged: Pop={stats.get('population')} Know={stats.get('knowledge'):.4f}", end="\r")
                            
                    except asyncio.TimeoutError:
                        continue
                    except Exception as e:
                        print(f"\nError receiving: {e}")
                        break
                        
        except Exception as e:
            print(f"\nConnection error: {e}. Retrying in 1s...")
            time.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(log_evolution())
    except KeyboardInterrupt:
        print("\nLogging stopped.")
