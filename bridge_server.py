import time
import random
import requests
import json
from prime_harmonics import EpistemicPhysics

# Configuration
WEB_SERVER_URL = "http://localhost:3000/api/simulation/update"
DIARY_URL = "http://localhost:3000/api/simulation/diary"
TICK_RATE = 2 # seconds

# Initial State
components = [97, 85, 75, 40, 20]

def push_update(data):
    try:
        requests.post(WEB_SERVER_URL, json=data, timeout=1)
    except Exception as e:
        print(f"Failed to push update: {e}")

def push_diary(entry_type, message, metrics=None):
    # Log to local file first
    EpistemicPhysics.log_diary_entry(entry_type, message, metrics)
    
    # Push to web
    payload = {
        "type": entry_type,
        "message": message,
        "metrics": metrics
    }
    try:
        requests.post(DIARY_URL, json=payload, timeout=1)
    except Exception as e:
        print(f"Failed to push diary: {e}")

print("Starting HARMONIA Research Bridge...")
push_diary("SYSTEM", "Research Bridge Online. Connecting to Console.")

while True:
    # 1. Simulate Fluctuation
    noise = random.uniform(-2, 2)
    components[3] += noise # Comms fluctuates
    components[3] = max(0, min(100, components[3]))
    
    # 2. Run Physics
    result = EpistemicPhysics.simulate_paradigm_stability(components)
    
    # 3. Push Data to Web Console
    push_update({
        "components": {
            "math": components[0],
            "physics": components[1],
            "futures": components[2],
            "comms": components[3],
            "implications": components[4]
        },
        "metrics": result
    })
    
    # 4. Log significant events
    if result['status'] != "STABLE" and random.random() < 0.3:
        push_diary("INSTABILITY", f"Stability Critical: {result['stability_score']:.4f}. Reinforce Comms Layer.", result)
    elif result['status'] == "STABLE" and random.random() < 0.3:
        push_diary("STABILITY", f"System Stabilized. Resonance: {result['resonance']:.4f}", result)
        
    print(f"Tick: {result['stability_score']:.4f}")
    time.sleep(TICK_RATE)
