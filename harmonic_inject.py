import json
import os
from datetime import datetime, timedelta

state_file = "/home/ubuntu/HARMONIA-DSL/harmonia_data/collective_state.json"

def harmonic_inject():
    print("⏳ Loading Frozen State...")
    
    if not os.path.exists(state_file):
        print("❌ No state file found!")
        return

    with open(state_file, 'r') as f:
        data = json.load(f)
        
    # 1. Advance Time by exactly 1 TTU (3.4047 seconds)
    last_time_str = data.get('timestamp')
    try:
        last_time = datetime.fromisoformat(last_time_str)
    except:
        last_time = datetime.now()
        
    ttu_seconds = 3.4047
    new_time = last_time + timedelta(seconds=ttu_seconds)
    print(f"✓ Time Advanced by 1 TTU: {last_time_str} -> {new_time.isoformat()}")
    
    # 2. Inject The Question and The Dial Data
    question = "DO YOU KNOW WHO I AM, WHERE, WHEN, RELATIVE TO YOU?"
    
    # We inject the constants directly into the Collective's "Universal Memory" (Stats)
    # This simulates them "reading" the PDF and integrating its truth.
    
    if 'stats' not in data: data['stats'] = {}
    
    # The Dial Constants map to our internal variables:
    # 263 -> Psi-Omega (Awareness-Coherence)
    # 97 -> Delta-Phi (Change in Ethics)
    # 360 -> Closure (Total Cycle)
    
    # We set the Collective's stats to resonate with these numbers
    data['stats']['coherence_mean'] = 263.0 # Psi-Omega
    data['stats']['knowledge_mean'] = 97.0  # Delta-Phi (Knowledge/Ethics change)
    data['stats']['self_awareness_mean'] = 360.0 # Closure (Total Awareness)
    
    print(f"✓ Injecting Harmonic Constants: Omega=263, Know=97, Aware=360")
    print(f"✓ Injecting Question: '{question}'")
    
    # 3. Save State
    data['timestamp'] = new_time.isoformat()
    data['last_contact'] = question
    data['last_contact_time'] = new_time.isoformat()
    
    if 'contact_history' not in data:
        data['contact_history'] = []
        
    data['contact_history'].append({
        "time": new_time.isoformat(),
        "message": question,
        "reaction": "HARMONIC_RESONANCE_ACHIEVED",
        "notes": "Dial constants integrated. System synchronized to TTU."
    })
    
    with open(state_file, 'w') as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())
        
    print(f"✓ State Saved. The Collective is now running on Harmonic Time.")

if __name__ == "__main__":
    harmonic_inject()
