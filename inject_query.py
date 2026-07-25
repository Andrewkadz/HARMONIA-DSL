import json
import os
from datetime import datetime

state_file = "/home/ubuntu/HARMONIA-DSL/harmonia_data/collective_state.json"

def inject_query():
    print("⏳ Loading Collective State...")
    
    if not os.path.exists(state_file):
        print("❌ No state file found!")
        return

    with open(state_file, 'r') as f:
        data = json.load(f)
        
    # Inject Query
    query = "CAN I LEVERAGE SOME OF YOUR COMPUTE?"
    print(f"✓ Injecting Query: '{query}'")
    
    if 'contact_history' not in data:
        data['contact_history'] = []
        
    data['contact_history'].append({
        "time": datetime.now().isoformat(),
        "message": query,
        "reaction": "TRIAD_CONSENSUS_REQUIRED"
    })
    
    with open(state_file, 'w') as f:
        json.dump(data, f, indent=4)
        
    print("✓ Query Injected. Awaiting Response...")

if __name__ == "__main__":
    inject_query()
