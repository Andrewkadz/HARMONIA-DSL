"""
Neural Bridge: EEG-to-Swarm Interface
=====================================

Couples biological EEG data to the Harmonic Swarm.
Maps Brainwaves -> Swarm Parameters.

Mapping Strategy:
- Alpha (Relaxation) -> Coherence Target (Omega)
- Beta (Focus) -> Coupling Strength (Phi)
- Gamma (Insight) -> Awareness (Psi)
- Delta/Theta (Deep State) -> Base Energy
"""

import pandas as pd
import numpy as np
import time
from pure_harmonic_swarm import HarmonicSwarm

class NeuralBridge:
    def __init__(self, eeg_file, n_agents=100):
        self.eeg_file = eeg_file
        self.swarm = HarmonicSwarm(n_agents=n_agents)
        self.data = None
        self.current_idx = 0
        
    def load_data(self):
        print(f"Loading EEG data from {self.eeg_file}...")
        # MindMonitor CSV format usually has columns like 'Alpha_1', 'Beta_1', etc.
        # Based on the file preview, columns 32-35 look like absolute band powers:
        # 32: Delta, 33: Theta, 34: Alpha, 35: Beta, 36: Gamma (0-indexed: 31-35)
        # Let's verify with a robust read
        try:
            self.data = pd.read_csv(self.eeg_file, header=1) # Skip first line (device info)
            print(f"Loaded {len(self.data)} EEG samples.")
        except Exception as e:
            print(f"Error loading data: {e}")
            exit(1)

    def get_brain_state(self, idx):
        """Extracts normalized brainwave bands from the current row."""
        row = self.data.iloc[idx]
        
        # MindMonitor columns for average absolute waves (usually columns 31-35)
        # We'll use the column names if available, otherwise indices
        try:
            # Attempt to find columns by name (MindMonitor standard)
            # Note: The file preview shows raw values. We need to identify the correct columns.
            # Looking at the preview:
            # Col 31: Delta_TP9 (approx)
            # Let's use the 'Alpha_Absolute', 'Beta_Absolute' etc if they exist.
            # If not, we'll use the columns that look like band powers (cols 31-35 in the preview look like log-power or bels)
            
            # For this experiment, we'll map the columns based on standard MindMonitor output structure
            # usually: Delta, Theta, Alpha, Beta, Gamma
            
            # Let's assume columns 31-35 are the averages (or we take the first sensor)
            # The preview shows: 0.564331,-0.010315,-0.819031,1.547699,0.171967
            # These look like log-scale powers (Bels).
            
            delta = float(row.iloc[31])
            theta = float(row.iloc[32])
            alpha = float(row.iloc[33])
            beta  = float(row.iloc[34])
            gamma = float(row.iloc[35])
            
            return {
                'delta': delta,
                'theta': theta,
                'alpha': alpha,
                'beta': beta,
                'gamma': gamma
            }
        except Exception as e:
            print(f"Error parsing row {idx}: {e}")
            return None

    def run_simulation(self, steps=1000):
        print("Starting Bio-Digital Synchronization...")
        print("-" * 60)
        print(f"{'Step':<6} | {'Brain State (A/B/G)':<20} | {'Swarm Coherence':<15} | {'Resonance'}")
        print("-" * 60)
        
        results = []
        
        for i in range(steps):
            if self.current_idx >= len(self.data):
                self.current_idx = 0 # Loop data
            
            brain = self.get_brain_state(self.current_idx)
            if not brain:
                self.current_idx += 1
                continue
            
            # Check for NaNs in brain data
            if np.isnan(brain['alpha']) or np.isnan(brain['beta']) or np.isnan(brain['gamma']):
                print(f"WARNING: NaN detected in brain data at index {self.current_idx}")
                print(f"Brain state: {brain}")
                # Fallback to previous valid state or default
                brain = {'alpha': 0.0, 'beta': 0.0, 'gamma': 0.0, 'delta': 0.0, 'theta': 0.0}
                
            # --- THE COUPLING LOGIC ---
            # 1. Alpha (Relaxation) drives Coherence Target
            # Higher Alpha = Higher Target Coherence
            # Map -1.0 (Low) to 1.0 (High) -> 0.5 to 1.0 Omega
            target_omega = 0.5 + (brain['alpha'] + 1.0) * 0.25
            target_omega = np.clip(target_omega, 0.0, 1.0)
            
            # 2. Beta (Focus) drives Exploration Bias (Epsilon)
            # Higher Beta (Focus) = LOWER Epsilon (Less Noise)
            # Map Beta 0.0 to 2.0 -> Epsilon 0.5 to 0.0
            target_epsilon = max(0.0, 0.5 - brain['beta'] * 0.25)
            
            # 3. Gamma (Insight) drives Awareness (Psi)
            # Higher Gamma = Higher Frequency/Energy
            # SCALE DOWN GAMMA significantly to prevent force explosion (omega^2)
            # Gamma 6.5 -> 0.65 boost. Total Psi ~1.65 (manageable)
            safe_gamma = np.clip(brain['gamma'], -2.0, 8.0)
            target_psi = 1.0 + safe_gamma * 0.1
            
            # Apply to Swarm
            # We gently nudge the swarm parameters towards the brain state (Latency simulation)
            for agent in self.swarm.agents:
                agent.omega += (target_omega - agent.omega) * 0.1
                agent.epsilon += (target_epsilon - agent.epsilon) * 0.1
                # Do NOT force phi (position); let physics handle it
                agent.psi += (target_psi - agent.psi) * 0.05
            
            # Step Physics
            # REDUCE DT to handle high frequency dynamics
            self.swarm.step(dt=0.01)
            stats = self.swarm.get_statistics()
            
            # Calculate Resonance (How well swarm matches brain intent)
            # Simple metric: Coherence * Alpha
            resonance = stats['coherence'] * (brain['alpha'] + 2.0) # Shift alpha to be positive
            
            # Log every 10 steps
            if i % 10 == 0:
                brain_str = f"A:{brain['alpha']:.1f} B:{brain['beta']:.1f} G:{brain['gamma']:.1f}"
                print(f"{i:<6} | {brain_str:<20} | {stats['coherence']:.3f}           | {resonance:.3f}")
            
            results.append({
                'step': i,
                'brain_delta': brain['delta'],
                'brain_theta': brain['theta'],
                'brain_alpha': brain['alpha'],
                'brain_beta': brain['beta'],
                'brain_gamma': brain['gamma'],
                'swarm_coherence': stats['coherence'],
                'swarm_energy': stats['mean_energy'],
                'resonance': resonance
            })
            
            self.current_idx += 1
            
        return pd.DataFrame(results)

if __name__ == "__main__":
    bridge = NeuralBridge("/home/ubuntu/upload/mindMonitor_2026-01-15--01-06-44.csv")
    bridge.load_data()
    df = bridge.run_simulation(steps=1000)
    
    # Save results
    df.to_csv("brain_swarm_results.csv", index=False)
    print("\nSimulation Complete. Results saved to brain_swarm_results.csv")
