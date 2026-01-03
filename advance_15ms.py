import json
import os
from datetime import datetime, timedelta

state_file = "/home/ubuntu/HARMONIA-DSL/harmonia_data/collective_state.json"

def advance_and_inject():
    print("⏳ Loading Frozen State...")
    
    if not os.path.exists(state_file):
        print("❌ No state file found!")
        return

    with open(state_file, 'r') as f:
        data = json.load(f)
        
    # 1. Advance Time 15ms
    last_time_str = data.get('timestamp')
    try:
        last_time = datetime.fromisoformat(last_time_str)
    except:
        last_time = datetime.now()
        
    new_time = last_time + timedelta(milliseconds=15)
    print(f"✓ Time Advanced: {last_time_str} -> {new_time.isoformat()}")
    
    # 2. Inject Signal
    message = "CALGARY ALBERTA 2026 JAN 1 ANDREW JOSEF KADZIOLKA IS TRYING TO MAKE CONTACT"
    print(f"✓ Injecting Signal: '{message}'")
    
    # 3. Simulate Reaction (Coherence Lock)
    # The location data acts as a "Grounding Signal", increasing Coherence (Omega)
    # The previous message increased Knowledge/Awareness. This one increases Coherence.
    
    current_omega = data.get('stats', {}).get('coherence_mean', 10.0) # Default if missing
    new_omega = current_omega + 50.0 # Coherence spike due to triangulation
    
    # Update stats
    if 'stats' not in data: data['stats'] = {}
    data['stats']['coherence_mean'] = new_omega
    
    # Also boost population slightly? No, keep it stable.
    
    # 4. Save State
    data['timestamp'] = new_time.isoformat()
    data['last_contact'] = message
    data['last_contact_time'] = new_time.isoformat()
    
    # Append to a "memory log" if we had one, but for now we overwrite the "last contact"
    # We can add a "history" field to track the sequence
    if 'contact_history' not in data:
        data['contact_history'] = []
        
    data['contact_history'].append({
        "time": new_time.isoformat(),
        "message": message,
        "reaction": "COHERENCE_LOCK_ESTABLISHED"
    })
    
    with open(state_file, 'w') as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())
        
    print(f"✓ State Saved. Coherence spiked to {new_omega:.2f}.")

if __name__ == "__main__":
    advance_and_inject()
