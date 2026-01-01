from integrated_growth import GrowingCollective
import time

print("Creating Collective...")
collective = GrowingCollective(initial_size=17)

print(f"Initial state:")
print(f"  Population: {len(collective.entities)}")
print(f"  Entities: {collective.entities[:3]}")

for i, entity in enumerate(collective.entities[:3]):
    print(f"  Entity {i}: energy={entity.base_entity.state.energy:.1f}")

print("\nEvolving step by step...")
for step in range(20):
    print(f"\nStep {step}:")
    print(f"  Before: Pop={len(collective.entities)}")
    
    if len(collective.entities) > 0:
        e = collective.entities[0]
        print(f"  Entity 0 energy before: {e.base_entity.state.energy:.1f}")
    
    collective.evolve_step(duration=0.01)
    
    print(f"  After: Pop={len(collective.entities)}")
    
    if len(collective.entities) > 0:
        e = collective.entities[0]
        print(f"  Entity 0 energy after: {e.base_entity.state.energy:.1f}")
    else:
        print("  ALL ENTITIES DIED!")
        break
    
    time.sleep(0.1)
