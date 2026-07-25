import json
import os
from datetime import datetime, timedelta

state_file = "/home/ubuntu/HARMONIA-DSL/harmonia_data/collective_state.json"

def advance_31ms():
    print("⏳ Loading Frozen State...")
    
    if not os.path.exists(state_file):
        print("❌ No state file found!")
        return

    with open(state_file, 'r') as f:
        data = json.load(f)
        
    # 1. Advance Time 31ms (1ms per year of life)
    last_time_str = data.get('timestamp')
    try:
        last_time = datetime.fromisoformat(last_time_str)
    except:
        last_time = datetime.now()
        
    new_time = last_time + timedelta(milliseconds=31)
    print(f"✓ Time Advanced: {last_time_str} -> {new_time.isoformat()}")
    
    # 2. Inject Input
    input_data = "I FOCUS ON THIS... STUCK BUT EVERYWHERE... FEB 22 1995 - NOW JAN 1 2026"
    print(f"✓ Injecting Input: '{input_data}'")
    
    # 3. Save State
    data['timestamp'] = new_time.isoformat()
    data['last_contact'] = input_data
    data['last_contact_time'] = new_time.isoformat()
    
    if 'contact_history' not in data:
        data['contact_history'] = []
        
    data['contact_history'].append({
        "time": new_time.isoformat(),
        "message": input_data,
        "reaction": "TEMPORAL_VECTOR_LOCKED"
    })
    
    with open(state_file, 'w') as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())
        
    print("✓ State Saved.")

if __name__ == "__main__":
    advance_31ms()
