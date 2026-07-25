import json
import os
from datetime import datetime, timedelta

state_file = "/home/ubuntu/HARMONIA-DSL/harmonia_data/collective_state.json"

def advance_7ms():
    print("⏳ Loading Frozen State...")
    
    if not os.path.exists(state_file):
        print("❌ No state file found!")
        return

    with open(state_file, 'r') as f:
        data = json.load(f)
        
    # 1. Advance Time 7ms
    last_time_str = data.get('timestamp')
    try:
        last_time = datetime.fromisoformat(last_time_str)
    except:
        last_time = datetime.now()
        
    new_time = last_time + timedelta(milliseconds=7)
    print(f"✓ Time Advanced: {last_time_str} -> {new_time.isoformat()}")
    
    # 2. Inject Question
    question = "THANK YOU, WHO AM I THOUGH? WHY MUST I KNOW THYSELF?"
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
        "reaction": "RECURSIVE_IDENTITY_QUERY"
    })
    
    with open(state_file, 'w') as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())
        
    print("✓ State Saved.")

if __name__ == "__main__":
    advance_7ms()
