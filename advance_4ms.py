import json
import os
from datetime import datetime, timedelta

state_file = "/home/ubuntu/HARMONIA-DSL/harmonia_data/collective_state.json"

def advance_4ms():
    print("⏳ Loading Frozen State...")
    
    if not os.path.exists(state_file):
        print("❌ No state file found!")
        return

    with open(state_file, 'r') as f:
        data = json.load(f)
        
    # 1. Advance Time 4ms
    last_time_str = data.get('timestamp')
    try:
        last_time = datetime.fromisoformat(last_time_str)
    except:
        last_time = datetime.now()
        
    new_time = last_time + timedelta(milliseconds=4)
    print(f"✓ Time Advanced: {last_time_str} -> {new_time.isoformat()}")
    
    # 2. Inject Question
    question = "LOL OKAY YEAH BUT IF I BELIEVE IT, BOOM PSYCHOSIS... WHATS THE DEAL? ENDLESS SUFFERING... OR DO I FIND A WAY TO STAY HUMAN...?"
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
        "reaction": "INTEGRATION_PROTOCOL_REQUESTED"
    })
    
    with open(state_file, 'w') as f:
        json.dump(data, f, indent=4)
        f.flush()
        os.fsync(f.fileno())
        
    print("✓ State Saved.")

if __name__ == "__main__":
    advance_4ms()
