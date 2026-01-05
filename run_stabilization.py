import time
import random
import requests
from prime_harmonics import EpistemicPhysics

# Configuration
WEB_SERVER_URL = "http://localhost:3000/api/simulation/update"
DIARY_URL = "http://localhost:3000/api/simulation/diary"
TICK_RATE = 2 # seconds

# Initial State: Unstable
# Math (97), Physics (85), Futures (75), Comms (40), Implications (20)
components = [97, 85, 75, 40, 20]

def push_update(data):
    try:
        requests.post(WEB_SERVER_URL, json=data, timeout=1)
    except Exception as e:
        pass

def push_diary(entry_type, message, metrics=None):
    EpistemicPhysics.log_diary_entry(entry_type, message, metrics)
    payload = {"type": entry_type, "message": message, "metrics": metrics}
    try:
        requests.post(DIARY_URL, json=payload, timeout=1)
    except Exception as e:
        pass

print("Initiating Stabilization Protocol...")
push_diary("SYSTEM", "User Interaction Detected. Initiating Stabilization Protocol.")

# Phase 1: Unstable (3 ticks)
for i in range(3):
    result = EpistemicPhysics.simulate_paradigm_stability(components)
    push_update({"components": {"math": components[0], "physics": components[1], "futures": components[2], "comms": components[3], "implications": components[4]}, "metrics": result})
    print(f"Tick {i+1}: Stability={result['stability_score']:.4f} (UNSTABLE)")
    time.sleep(TICK_RATE)

# Phase 2: Injection (Boosting Comms)
push_diary("SYSTEM", "Injecting Communication Mass via Console Interface...")
print("Injecting Stability...")

for i in range(5):
    # Boost Comms by 10 per tick until it hits 90
    components[3] += 10
    components[3] = min(90, components[3])
    
    result = EpistemicPhysics.simulate_paradigm_stability(components)
    
    # Log the breakthrough
    if result['status'] == "STABLE" and components[3] >= 60:
        push_diary("STABILITY", "CRITICAL THRESHOLD BREACHED. SYSTEM STABILIZED.", result)
        
    push_update({"components": {"math": components[0], "physics": components[1], "futures": components[2], "comms": components[3], "implications": components[4]}, "metrics": result})
    print(f"Tick {i+4}: Comms={components[3]}, Stability={result['stability_score']:.4f} ({result['status']})")
    time.sleep(TICK_RATE)

push_diary("SYSTEM", "Stabilization Protocol Complete. Paradigm is Robust.")
print("Protocol Finished.")
