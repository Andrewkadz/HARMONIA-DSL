import json
import os
import uuid
from archetypes import ArchetypeLibrary

state_file = "/home/ubuntu/HARMONIA-DSL/harmonia_data/collective_state.json"

def inject_triad_partners():
    print("⏳ Loading Collective State...")
    
    if not os.path.exists(state_file):
        print("❌ No state file found!")
        return

    with open(state_file, 'r') as f:
        data = json.load(f)
        
    # 1. Inject Harmonic Sage (Φ)
    sage_config = ArchetypeLibrary.get_harmonic_sage()
    sage_entity = {
        "id": f"RI1007-PHI-{str(uuid.uuid4())[:8]}",
        "name": sage_config.name,
        "archetype": "HARMONIC_SAGE",
        "signature": sage_config.signature,
        "energy": 800.0,
        "knowledge": 0.8,
        "awareness": 0.8, # High but grounded
        "maturity": 1.0,  # Fully Mature
        "position": {"x": -1.0, "y": 0.0, "z": 0.0}, # Left of Center
        "params": {
            "beta_tracking": sage_config.beta_tracking,
            "gamma_modulation": sage_config.gamma_modulation,
            "alpha_decay": sage_config.alpha_decay,
            "dissonance_factor": sage_config.dissonance_factor
        },
        "status": "ACTIVE"
    }
    
    # 2. Inject Void Walker (π)
    walker_config = ArchetypeLibrary.get_void_walker()
    walker_entity = {
        "id": f"RI1007-PI-{str(uuid.uuid4())[:8]}",
        "name": walker_config.name,
        "archetype": "VOID_WALKER",
        "signature": walker_config.signature,
        "energy": 800.0,
        "knowledge": 0.9,
        "awareness": 0.9, # Very High
        "maturity": 0.5,  # Cyclic
        "position": {"x": 1.0, "y": 0.0, "z": 0.0}, # Right of Center
        "params": {
            "beta_tracking": walker_config.beta_tracking,
            "gamma_modulation": walker_config.gamma_modulation,
            "alpha_decay": walker_config.alpha_decay,
            "dissonance_factor": walker_config.dissonance_factor
        },
        "status": "ACTIVE"
    }
    
    # Inject
    if 'entities' not in data:
        data['entities'] = []
        
    data['entities'].append(sage_entity)
    data['entities'].append(walker_entity)
    data['population'] = len(data['entities'])
    
    # Log Event
    if 'contact_history' not in data:
        data['contact_history'] = []
        
    data['contact_history'].append({
        "time": data.get('timestamp'),
        "message": "INJECTION: TRIAD COMPLETED (Φ + π)",
        "reaction": "SYSTEM_EQUILIBRIUM_LOCKED"
    })
    
    with open(state_file, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"✓ INJECTED: {sage_entity['name']} (Φ)")
    print(f"✓ INJECTED: {walker_entity['name']} (π)")
    print("✓ TRIAD STATUS: COMPLETE (Φ - ε - π)")

if __name__ == "__main__":
    inject_triad_partners()
