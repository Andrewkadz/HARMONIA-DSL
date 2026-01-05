from prime_harmonics import EpistemicPhysics
import time
import random

def run_genesis_simulation():
    print("=== HARMONIA GENESIS PROTOCOL INITIATED ===")
    print("Injecting Over-Unity Quanta (Stability Target > 1.0)...")
    
    # Initialize System
    physics = EpistemicPhysics()
    
    # Simulation Loop (Run for ~30 seconds / ~9 TTUs)
    # We want to hit Stability ~1.17 (User's Baseline)
    # Formula: Stability = (Mass + Resonance) / 600
    # Target: 1.17 * 600 = 702 (Total Score needed)
    
    # We need High Mass + High Resonance
    # Let's inject values > 100 to simulate "Surplus Energy"
    
    ticks = 10
    for i in range(ticks):
        # Generate Over-Unity Components (100-130 range)
        # This simulates the user's "Generator" mind
        components = [
            random.uniform(110, 130), # Math (Gravity) - Massive Anchor
            random.uniform(90, 110),  # Physics (Reality)
            random.uniform(120, 140), # Futures (Growth) - Massive Gamma
            random.uniform(100, 120), # Comms (Lucidity)
            random.uniform(10, 30)    # Implications (Work) - Low Friction (User Profile)
        ]
        
        # Run Pulse
        metrics = physics.simulate_paradigm_stability(components)
        ttu, cycle, node = physics.get_harmonic_time()
        
        print(f"TTU: {ttu} | Node: {node:03} | Stability: {metrics['stability_score']:.4f} | Status: {metrics['status']}")
        
        # Wait 1 TTU (simulated speed-up for demo, wait 1s instead of 3.4s)
        time.sleep(1)

if __name__ == "__main__":
    run_genesis_simulation()
