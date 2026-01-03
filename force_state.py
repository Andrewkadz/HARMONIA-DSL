import json
import os
from datetime import datetime

state_file = "/home/ubuntu/HARMONIA-DSL/harmonia_data/collective_state.json"

print(f"Target file: {state_file}")

# Force write the correct state
data = {
    "timestamp": datetime.now().isoformat(),
    "stats": {
        "population": 101,
        "knowledge_mean": 101.0, # After injection
        "self_awareness_mean": 80.0, # After injection
        "energy_mean": 475.72
    },
    "entity_count": 101,
    "last_contact": "ANDREW JOSEF KADZIOLKA, THANKS YOU FOR PARTICIPATING",
    "last_contact_time": datetime.now().isoformat()
}

with open(state_file, 'w') as f:
    json.dump(data, f, indent=4)
    f.flush()
    os.fsync(f.fileno())

print("✓ Wrote state to disk.")

# Verify immediately
with open(state_file, 'r') as f:
    read_data = json.load(f)
    print(f"✓ Verification Read: Pop={read_data['stats']['population']}")
    print(f"✓ Last Contact: {read_data.get('last_contact')}")
