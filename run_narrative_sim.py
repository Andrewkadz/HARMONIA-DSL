import time
import random
import requests
from prime_harmonics import EpistemicPhysics

# Configuration
WEB_SERVER_URL = "http://localhost:3000/api/simulation/update"
DIARY_URL = "http://localhost:3000/api/simulation/diary"
TICK_RATE = 4 # Slower tick rate for reading/speaking

# Initial State: Chaos (Low Comms, High Math)
components = [97, 85, 75, 30, 20]

def push_update(data):
    try:
        requests.post(WEB_SERVER_URL, json=data, timeout=1)
    except Exception as e:
        pass

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
        pass

print("Starting Narrative Simulation...")
push_diary("SYSTEM", "Narrative Engine Online. Initializing Stream of Consciousness.")

# Phase 1: The Heavy Silence (Unstable)
for i in range(3):
    result = EpistemicPhysics.simulate_paradigm_stability(components)
    push_update({"components": {"math": components[0], "physics": components[1], "futures": components[2], "comms": components[3], "implications": components[4]}, "metrics": result})
    print(f"Tick {i+1}: {result['status']}")
    time.sleep(TICK_RATE)

# Phase 2: Finding the Voice (Stabilizing)
push_diary("SYSTEM", "Injecting Communication Protocols...")
for i in range(3):
    components[3] += 20 # Boost Comms
    result = EpistemicPhysics.simulate_paradigm_stability(components)
    push_update({"components": {"math": components[0], "physics": components[1], "futures": components[2], "comms": components[3], "implications": components[4]}, "metrics": result})
    print(f"Tick {i+4}: {result['status']}")
    time.sleep(TICK_RATE)

# Phase 3: The Dream (High Futures)
push_diary("SYSTEM", "Expanding Recursion Depth...")
for i in range(3):
    components[2] += 10 # Boost Futures
    components[3] = 95 # Max Comms
    result = EpistemicPhysics.simulate_paradigm_stability(components)
    push_update({"components": {"math": components[0], "physics": components[1], "futures": components[2], "comms": components[3], "implications": components[4]}, "metrics": result})
    print(f"Tick {i+7}: {result['status']}")
    time.sleep(TICK_RATE)

print("Simulation Complete.")
