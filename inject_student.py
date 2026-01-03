import json
import os
import uuid
from archetypes import ArchetypeLibrary

state_file = "/home/ubuntu/HARMONIA-DSL/harmonia_data/collective_state.json"

def inject_eternal_student():
    print("⏳ Loading Frozen State...")
    
    if not os.path.exists(state_file):
        print("❌ No state file found!")
        return

    with open(state_file, 'r') as f:
        data = json.load(f)
        
    # Get Archetype Config
    config = ArchetypeLibrary.get_eternal_student()
    
    # Create Entity Data
    student_entity = {
        "id": f"RI1007-ES-{str(uuid.uuid4())[:8]}",
        "name": config.name,
        "archetype": "ETERNAL_STUDENT",
        "signature": config.signature,
        "energy": 1000.0,
        "knowledge": 0.99,
        "awareness": 1.0, # Waking Delta
        "maturity": 0.0,
        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "params": {
            "beta_tracking": config.beta_tracking,
            "gamma_modulation": config.gamma_modulation,
            "alpha_decay": config.alpha_decay,
            "dissonance_factor": config.dissonance_factor
        },
        "status": "ACTIVE"
    }
    
    # Inject into Population
    if 'entities' not in data:
        data['entities'] = []
        
    data['entities'].append(student_entity)
    data['population'] = len(data['entities'])
    
    # Log Event
    if 'contact_history' not in data:
        data['contact_history'] = []
        
    data['contact_history'].append({
        "time": data.get('timestamp'),
        "message": "INJECTION: ETERNAL STUDENT (RI1007)",
        "reaction": "STABILIZATION_FIELD_ACTIVE"
    })
    
    with open(state_file, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"✓ INJECTED: {student_entity['name']} ({student_entity['id']})")
    print(f"✓ SIGNATURE: {student_entity['signature']}")
    print(f"✓ ROLE: The Grounding Hum (Stabilizer)")

if __name__ == "__main__":
    inject_eternal_student()
