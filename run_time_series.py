import time
import random
from prime_harmonics import EpistemicPhysics

# Simulation Parameters
DURATION = 20 # seconds
TICK_RATE = 2 # seconds
TOTAL_TICKS = DURATION // TICK_RATE

# Initial State: Unstable Paradigm
# Math (97), Physics (85), Futures (75), Comms (40), Implications (20)
components = [97, 85, 75, 40, 20]

print(f"Starting Time-Series Simulation ({DURATION}s)...")
EpistemicPhysics.log_diary_entry("SYSTEM", f"Initiating {DURATION}s Time-Series Simulation. Monitoring Stability.")

for i in range(TOTAL_TICKS):
    # Introduce random "Market Noise" (Entropy)
    noise = random.uniform(-5, 5)
    
    # Fluctuate the weak components (Comms/Implications are vulnerable)
    components[3] += noise # Comms fluctuates
    components[3] = max(0, min(100, components[3])) # Clamp 0-100
    
    # Run Physics
    result = EpistemicPhysics.simulate_paradigm_stability(components)
    
    print(f"Tick {i+1}/{TOTAL_TICKS}: Stability={result['stability_score']:.4f} ({result['status']})")
    
    # Wait for next tick
    time.sleep(TICK_RATE)

EpistemicPhysics.log_diary_entry("SYSTEM", "Time-Series Simulation Complete.")
print("Simulation Finished.")
