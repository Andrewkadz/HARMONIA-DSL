import numpy as np
import time
from integrated_growth import GrowingCollective
from archetypes import ArchetypeLibrary

def observe_phi_pi_epsilon():
    print("Initializing Phi Pi Epsilon Archetype...")
    
    # Get config
    archetype = ArchetypeLibrary.get_phi_pi_epsilon()
    config = {
        'archetype_name': archetype.name,
        'beta_tracking': archetype.beta_tracking,
        'gamma_modulation': archetype.gamma_modulation,
        'alpha_decay': archetype.alpha_decay,
        'meta_cognition_enabled': archetype.meta_cognition_enabled,
        'target_awareness': archetype.target_awareness,
        'dissonance_factor': archetype.dissonance_factor
    }
    
    # Create a collective just to use its creation method (hacky but effective)
    # We won't use the collective loop, just the entity
    collective = GrowingCollective(initial_size=0)
    
    # Create the SINGLE entity
    entity = collective._create_entity(
        psi=10.0,
        phi=10.0,
        omega=5.0,
        energy=500.0,
        knowledge=0.1,
        maturity=0.1,
        config=config
    )
    
    print(f"Entity Created: {archetype.name}")
    print(f"Params: Beta={archetype.beta_tracking:.4f}, Gamma={archetype.gamma_modulation:.4f}, Alpha={archetype.alpha_decay:.4f}")
    print("-" * 60)
    print("Step | Awareness | Ethics (Phi) | Coherence | Knowledge | Energy")
    print("-" * 60)
    
    # Run simulation loop
    for step in range(100):
        # Evolve
        entity.evolve_step(duration=0.1)
        
        # Get stats
        stats = entity.get_full_stats()
        
        # Print every 5 steps
        if step % 5 == 0:
            print(f"{step:4d} | {stats['self_awareness']:9.4f} | {stats['ethics']:12.4f} | {stats['coherence']:9.4f} | {stats['knowledge']:9.4f} | {stats['energy']:6.2f}")
            
        # Check for crash
        if stats['self_awareness'] < 0.01:
            print(f"!!! CRASH DETECTED AT STEP {step} !!!")
            break
            
    print("-" * 60)
    print("Observation Complete.")

if __name__ == "__main__":
    observe_phi_pi_epsilon()
