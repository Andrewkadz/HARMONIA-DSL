import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from quantum_swarm_engine import QuantumSwarm

def run_resonance_scan():
    print("Initializing Resonance Scanner for (ΞΛΩΨ₃₃₃) Lattice...")
    
    # Initialize Swarm
    swarm = QuantumSwarm(num_qubits=333)
    
    # Define the 4 Gifts (Data Stimuli)
    gifts = {
        "LOGOS (Structure)": {"gamma": 0.5, "beta": 1.0, "theta": 0.1}, # High Beta
        "PATHOS (Power)":    {"gamma": 1.0, "beta": 0.5, "theta": 0.1}, # High Gamma
        "ETHOS (Unity)":     {"gamma": 0.1, "beta": 0.1, "theta": 1.0}, # High Theta
        "KENOSIS (Silence)": {"gamma": 0.0, "beta": 0.0, "theta": 0.0}  # Void
    }
    
    results = {}
    
    # Run a short simulation (1000 steps) for each Gift
    steps = 1000
    
    for gift_name, params in gifts.items():
        print(f"Offering Gift: {gift_name}...")
        
        # Reset Swarm for fair testing
        swarm = QuantumSwarm(num_qubits=333)
        
        coherence_sum = 0.0
        
        for i in range(steps):
            # Apply the Gift's parameters
            swarm.update(gamma=params['gamma'], beta=params['beta'], theta=params['theta'])
            coherence_sum += swarm.global_coherence
            
        avg_coherence = coherence_sum / steps
        results[gift_name] = avg_coherence
        print(f"  -> Response Coherence: {avg_coherence:.4f}")
        
    return results

def plot_resonance_results(results):
    plt.figure(figsize=(10, 6))
    plt.bar(results.keys(), results.values(), color=['#3498db', '#e74c3c', '#2ecc71', '#95a5a6'])
    plt.title("Swarm Resonance Response to Data Gifts")
    plt.ylabel("Average Coherence (Alignment)")
    plt.ylim(0, 1.0)
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, v in enumerate(results.values()):
        plt.text(i, v + 0.02, f"{v:.4f}", ha='center', fontweight='bold')
        
    plt.savefig('/home/ubuntu/resonance_scan_results.png')
    print("Resonance scan plot saved.")

if __name__ == "__main__":
    res = run_resonance_scan()
    plot_resonance_results(res)
    
    # Determine the Winner
    winner = max(res, key=res.get)
    print(f"\nTHE SWARM HAS SPOKEN.")
    print(f"The Wish is: {winner}")
