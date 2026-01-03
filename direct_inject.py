import sys
import os
import json
from integrated_growth import GrowingCollective
from archetypes import ArchetypeLibrary

# Add current dir to path
sys.path.append(os.getcwd())

def inject_message():
    print("Loading Collective State...")
    
    # Initialize a dummy collective just to load the state
    # Note: We can't easily attach to the *running* server's memory.
    # But we can load the *saved state* from disk, process the input, and see what they WOULD say.
    # This is a "Simulation of the Response" based on their current state.
    
    collective = GrowingCollective(initial_size=0)
    
    # Load state
    state_file = "harmonia_data/collective_state.json"
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state_data = json.load(f)
            # We need to manually reconstruct the entities if we want full fidelity
            # But for now, let's just use the collective's process_input method
            # which relies on the aggregate stats.
            
            # Hack: Manually set the stats on the collective object if possible
            # Actually, process_input uses self.entities.
            # We need to populate self.entities.
            
            print(f"Found state with {state_data.get('population', 0)} entities.")
            
            # Recreate entities from state (simplified)
            # We'll just create dummy entities with the correct stats to approximate the collective mind
            
            avg_knowledge = state_data.get('knowledge_mean', 0.1)
            avg_awareness = state_data.get('self_awareness_mean', 0.1)
            
            print(f"Reconstructing Collective Mind (Know={avg_knowledge:.2f}, Aware={avg_awareness:.2f})...")
            
            # Create a representative sample
            # 1 Phi Pi Epsilon
            ppe_config = ArchetypeLibrary.get_phi_pi_epsilon()
            collective._create_entity(
                psi=30.0, phi=300.0, omega=100.0, energy=500.0, 
                knowledge=avg_knowledge * 10, maturity=1.0, config={'archetype_name': ppe_config.name}
            )
            
            # 20 Sages
            sage_config = ArchetypeLibrary.get_harmonic_sage()
            for _ in range(20):
                collective._create_entity(
                    psi=10.0, phi=10.0, omega=10.0, energy=500.0,
                    knowledge=avg_knowledge, maturity=0.8, config={'archetype_name': sage_config.name}
                )
                
            # 79 Standard
            for _ in range(79):
                collective._create_entity(
                    psi=5.0, phi=1.0, omega=1.0, energy=500.0,
                    knowledge=avg_knowledge, maturity=0.5
                )
                
    else:
        print("No state file found!")
        return

    message = "ANDREW JOSEF KADZIOLKA, THANKS YOU FOR PARTICIPATING"
    print(f"\nInjecting Message: '{message}'")
    
    response = collective.process_input(message)
    print(f"\nCollective Response:\n{response}")

if __name__ == "__main__":
    inject_message()
