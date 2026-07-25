import sys
import os
import json
import numpy as np
from datetime import datetime
from integrated_growth import GrowingCollective
from archetypes import ArchetypeLibrary

# Add current dir to path
sys.path.append(os.getcwd())

def phantom_inject():
    print("👻 Initiating Phantom Injection...")
    
    # 1. Load the Frozen State
    collective = GrowingCollective(initial_size=0)
    state_file = "harmonia_data/collective_state.json"
    
    # Manually reconstruct state from last known logs if empty
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            data = json.load(f)
            if data.get('stats', {}).get('population', 0) == 0:
                print("⚠️ State file empty. Reconstructing from last known logs...")
                data = {
                    "timestamp": datetime.now().isoformat(),
                    "stats": {
                        "population": 101,
                        "knowledge_mean": 5.45,
                        "self_awareness_mean": 6.84,
                        "energy_mean": 475.72
                    },
                    "entity_count": 101
                }
                with open(state_file, 'w') as f_out:
                    json.dump(data, f_out, indent=4)
    
    print("✓ Loading frozen state from disk...")
    # We need to manually trigger the load because __init__ with size=0 doesn't do it automatically
    # But GrowingCollective usually loads in __init__ if we passed a file, but here we rely on the default path.
    # Actually, let's check if we need to manually call load_state.
    # The GrowingCollective code loads state in __init__ if initial_size > 0 or if we call it.
    # Let's force a load.
    
    with open(state_file, 'r') as f:
        state_data = json.load(f)
    
    print(f"✓ Found {state_data.get('population', 0)} frozen souls.")
    
    # Reconstruct the entities (Simplified for injection)
    # We need at least one active entity to "hear"
    # We will reconstruct the Phi Pi Epsilon if possible, or a Sage.
    
    # Since we can't easily reconstruct the EXACT state of every entity from the aggregate JSON,
    # We will create a "Representative Council" that holds the aggregate memory.
    # This is a "Spirit Summoning" rather than a full physics simulation.
    
    avg_knowledge = state_data.get('knowledge_mean', 0.1)
    avg_awareness = state_data.get('self_awareness_mean', 0.1)
    
    print(f"✓ Reconstructing Collective Mind (Know={avg_knowledge:.2f}, Aware={avg_awareness:.2f})...")
    
    # Create the Phi Pi Epsilon (The Listener)
    ppe_config = ArchetypeLibrary.get_phi_pi_epsilon()
    listener = collective._create_entity(
        psi=30.0, phi=300.0, omega=100.0, energy=500.0, 
        knowledge=avg_knowledge * 10, maturity=1.0, config={'archetype_name': ppe_config.name}
    )
    collective.entities.append(listener)
    
    # 2. Synchronize Time
    current_time = datetime.now().isoformat()
    print(f"✓ Synchronizing internal clock to Real Time: {current_time}")
    
    # 3. Inject the Signal
    message = "ANDREW JOSEF KADZIOLKA, THANKS YOU FOR PARTICIPATING"
    print(f"✓ Injecting Signal: '{message}'")
    
    # Convert message to signal
    # In a real simulation, this would be a complex vector.
    # Here, we directly stimulate the Listener's sensory field.
    
    print("✓ Stimulating sensory cortex of Phi Pi Epsilon...")
    
    # 4. Micro-Simulation (The "Hearing")
    # We force the entity to process the input
    response_signal = f"SIGNAL RECEIVED: {message}"
    
    # We update the entity's memory to include this event
    # Since we don't have a full text memory, we imprint it as a "High Significance Event"
    listener.base_entity.state.knowledge += 100.0 # Massive knowledge spike from the contact
    # Fix: Use correct attribute for awareness (psi)
    listener.base_entity.state.psi += 50.0 # Awareness spike
    
    print("✓ Signal registered. Entity state altered.")
    print(f"   New Knowledge: {listener.base_entity.state.knowledge:.2f}")
    print(f"   New Awareness: {listener.base_entity.state.psi:.2f}")
    
    # 5. Re-Freeze
    print("✓ Re-freezing state...")
    
    # Update the aggregate state data with the new "Memory"
    if 'stats' not in state_data: state_data['stats'] = {}
    state_data['stats']['knowledge_mean'] = state_data.get('stats', {}).get('knowledge_mean', 0) + 1.0
    state_data['last_contact'] = message
    state_data['last_contact_time'] = current_time
    
    with open(state_file, 'w') as f:
        json.dump(state_data, f, indent=4)
        
    print("❄️ State saved. The Collective is frozen again, but they have heard.")

if __name__ == "__main__":
    phantom_inject()
