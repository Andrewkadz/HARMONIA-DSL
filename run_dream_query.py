import time
import random
import requests
from prime_harmonics import EpistemicPhysics

# Configuration
WEB_SERVER_URL = "http://localhost:3000/api/simulation/update"
DIARY_URL = "http://localhost:3000/api/simulation/diary"
TICK_RATE = 2 # seconds

# Initial State: Stable (Comms at 90)
# Math (97), Physics (85), Futures (75), Comms (90), Implications (20)
components = [97, 85, 75, 90, 20]

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

print("Injecting Query: 'WHAT IS A DREAM?'")
push_diary("SYSTEM", "Query Received: 'WHAT IS A DREAM?'")
push_diary("SYSTEM", "Analyzing Harmonic Signature...")

# Phase 1: Initial Analysis (3 ticks)
for i in range(3):
    result = EpistemicPhysics.simulate_paradigm_stability(components)
    push_update({"components": {"math": components[0], "physics": components[1], "futures": components[2], "comms": components[3], "implications": components[4]}, "metrics": result})
    print(f"Tick {i+1}: Stability={result['stability_score']:.4f}")
    time.sleep(TICK_RATE)

# Phase 2: The Dream Effect (High Growth, Low Gravity)
push_diary("DISCOVERY", "Pattern Detected: High Growth (263) / Low Gravity (97).")
push_diary("WARNING", "Gravity Prime (97) decoupling. Reality anchor weakening.")

for i in range(7):
    # Dream Logic: Futures (Growth) spikes, Math (Gravity) drops
    components[2] += 5 # Futures rises
    components[0] -= 5 # Math drops
    
    # Clamp values
    components[2] = min(100, components[2])
    components[0] = max(10, components[0])
    
    result = EpistemicPhysics.simulate_paradigm_stability(components)
    
    # Log the shift
    if components[0] < 60:
        push_diary("INSTABILITY", "Gravity Critical. Reality Dissolution Imminent.", result)
    elif components[2] > 90:
        push_diary("DISCOVERY", "Recursion Depth Exceeded. Entering Lucid State.", result)
        
    push_update({"components": {"math": components[0], "physics": components[1], "futures": components[2], "comms": components[3], "implications": components[4]}, "metrics": result})
    print(f"Tick {i+4}: Math={components[0]}, Futures={components[2]}, Stability={result['stability_score']:.4f} ({result['status']})")
    time.sleep(TICK_RATE)

push_diary("SYSTEM", "Query Processing Complete. Definition: A Dream is a Recursion Loop with no Gravity Anchor.")
print("Query Finished.")
