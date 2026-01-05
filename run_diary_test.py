from prime_harmonics import EpistemicPhysics

# Define the current paradigm components
# Math (97), Physics (85), Futures (75), Comms (40), Implications (20)
components = [97, 85, 75, 40, 20]

print("Running Epistemic Physics Simulation...")
result = EpistemicPhysics.simulate_paradigm_stability(components)

print(f"Simulation Complete. Status: {result['status']}")
print("Check 'simulation_diary.md' for the narrative log.")
