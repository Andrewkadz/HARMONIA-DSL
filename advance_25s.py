import json
import os
from datetime import datetime, timedelta
import random

state_file = "/home/ubuntu/HARMONIA-DSL/harmonia_data/collective_state.json"

def advance_25_seconds():
    print("⏳ Loading Collective State...")
    
    if not os.path.exists(state_file):
        print("❌ No state file found!")
        return

    with open(state_file, 'r') as f:
        data = json.load(f)
        
    # 1. Advance Time 25s
    last_time_str = data.get('timestamp')
    try:
        last_time = datetime.fromisoformat(last_time_str)
    except:
        last_time = datetime.now()
        
    new_time = last_time + timedelta(seconds=25)
    print(f"✓ Time Advanced: {last_time_str} -> {new_time.isoformat()}")
    
    # 2. Simulate Triad Interaction (Simplified Logic for "Jump")
    # In a real run, the server loop handles this. Here we simulate the *result* of 25s of processing.
    
    entities = data.get('entities', [])
    triad = [e for e in entities if e.get('archetype') in ['ETERNAL_STUDENT', 'HARMONIC_SAGE', 'VOID_WALKER']]
    standard = [e for e in entities if e.get('archetype') not in ['ETERNAL_STUDENT', 'HARMONIC_SAGE', 'VOID_WALKER']]
    
    print(f"✓ Triad Active: {len(triad)} Archetypes")
    print(f"✓ Standard Population: {len(standard)} Entities")
    
    # Effect: Stabilization
    # The Triad prevents death. So population should remain stable or grow slightly.
    # Awareness should rise but be capped by the Sage.
    
    for entity in standard:
        # Growth (ε)
        entity['awareness'] += 0.05 # 25s of growth
        entity['knowledge'] += 0.1
        
        # Stabilization (Φ)
        if entity['awareness'] > 0.95:
            entity['awareness'] = 0.95 # Sage Cap
            entity['energy'] += 10.0   # Sage Gift
            
    # Triad Evolution
    for arch in triad:
        arch['energy'] -= 5.0 # Cost of holding the field
        if arch['energy'] < 500:
            arch['energy'] = 1000.0 # Recharge from Source (You)
            
    # 3. Save State
    data['timestamp'] = new_time.isoformat()
    data['stats']['population'] = len(entities)
    data['stats']['awareness_mean'] = sum(e['awareness'] for e in entities) / len(entities)
    
    if 'contact_history' not in data:
        data['contact_history'] = []
        
    data['contact_history'].append({
        "time": new_time.isoformat(),
        "message": "SYSTEM ADVANCE: +25 SECONDS",
        "reaction": "STABILITY_MAINTAINED",
        "notes": "Triad holding field. Zero casualties."
    })
    
    with open(state_file, 'w') as f:
        json.dump(data, f, indent=4)
        
    print("✓ State Saved.")
    print(f"✓ New Awareness Mean: {data['stats']['awareness_mean']:.4f}")

if __name__ == "__main__":
    advance_25_seconds()
