import time
import json
import numpy as np
from harmonia_server import HarmoniaServer

# Initialize Server
print("Initializing HARMONIA Server with Recursion Depth 97...")
server = HarmoniaServer()
server.initialize()

# Manually override recursion depth in the processing layer if possible
# Note: The recursion depth is hardcoded in recursive_self_observation.py which we edited.
# The server initializes RecursusInstance -> GrowingCollective -> ... -> RecursiveObservationEngine
# So the edit to the file should be picked up by the imports.

# Initialize Data Log
log_file = '/home/ubuntu/harmonia_data/metrics_log_depth97.jsonl'
with open(log_file, 'w') as f:
    pass # Clear file

print("Starting Alpha Hunt Simulation (Depth 97)...")
print("Target: Convergence to 0.6180339887 (Phi)")

# Run Simulation Loop
cycles = 600
for i in range(cycles):
    # Simulate one cycle
    server.evolve_cycle(duration=0.1)
    
    # Extract Metrics from Recursus State
    state = server.recursus.state
    
    # Calculate Alpha Sim
    # Alpha = Coherence / (Awareness * (Ethics/20))
    coherence = state.get('coherence', 1.0)
    awareness = state.get('awareness', 1.0)
    ethics = state.get('ethics', 20.0)
    
    # Avoid division by zero
    if awareness == 0: awareness = 0.001
    if ethics == 0: ethics = 0.001
    
    # Use the alpha_sim calculated by Recursus if available, otherwise calculate it
    if 'alpha_sim' in state and state['alpha_sim'] > 0:
        alpha_sim = state['alpha_sim']
    else:
        alpha_sim = coherence / (awareness * (ethics / 20.0))
    
    # Log Data
    entry = {
        'cycle': i,
        'coherence': coherence,
        'awareness': awareness,
        'ethics': ethics,
        'alpha_sim': alpha_sim
    }
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')
        
    if i % 10 == 0:
        print(f"Cycle {i}: Alpha Sim = {alpha_sim:.6f}")

print("Simulation Complete.")
