import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

# --- SWARM PHYSICS ENGINE (Simplified for Simulation) ---
class CognitiveSwarm:
    def __init__(self, num_agents=100):
        self.num_agents = num_agents
        self.positions = np.random.rand(num_agents, 2) * 10 - 5  # Area -5 to 5
        self.velocities = np.random.randn(num_agents, 2) * 0.1
        self.coherence = 0.0
        self.entropy = 1.0
        
    def update(self, gamma, beta, theta):
        """
        Update swarm dynamics based on EEG signals.
        Gamma -> Speed (Energy)
        Beta -> Coupling (Alignment Force)
        Theta -> Radius (Field Expansion)
        """
        # Normalize inputs (approximate ranges based on analysis)
        # Gamma: 0.0 - 0.2
        # Beta: 0.0 - 0.2
        # Theta: 0.0 - 0.5
        
        speed_factor = 1.0 + (gamma * 20.0)  # High Gamma = Fast Swarm
        coupling_strength = beta * 5.0       # High Beta = Strong Alignment
        field_radius = 5.0 + (theta * 10.0)  # High Theta = Expanded Field
        
        # 1. Alignment Rule (Cohesion)
        center_mass = np.mean(self.positions, axis=0)
        to_center = center_mass - self.positions
        
        # 2. Separation Rule (Avoid Crowding)
        # Simple repulsion from origin if too close (simulating field pressure)
        dist_from_origin = np.linalg.norm(self.positions, axis=1)
        repulsion = self.positions * 0.01
        
        # Apply Forces
        # If Coupling is high, agents move towards center (Crystalize)
        # If Speed is high, random motion increases (Heat)
        
        alignment_force = to_center * coupling_strength * 0.05
        random_force = np.random.randn(self.num_agents, 2) * speed_factor * 0.1
        
        # Update Velocities
        self.velocities += alignment_force + random_force - repulsion
        
        # Dampening
        self.velocities *= 0.95
        
        # Update Positions
        self.positions += self.velocities
        
        # Boundary Condition (Soft Walls based on Theta)
        # If outside radius, push back hard
        mask = dist_from_origin > field_radius
        self.positions[mask] *= 0.9
        
        # Calculate System Metrics
        # Coherence = 1 / (std_dev of positions + epsilon)
        std_pos = np.std(self.positions)
        self.coherence = 1.0 / (std_pos + 0.1)
        
        # Entropy = Speed * Spread
        self.entropy = np.mean(np.linalg.norm(self.velocities, axis=1)) * std_pos

# --- DATA LOADER ---
def load_eeg_data(filepath):
    # Load the processed CSV (skipping header row 0)
    df = pd.read_csv(filepath, header=0)
    
    # Extract relevant columns (assuming standard layout)
    # 1-4: Delta, 5-8: Theta, 9-12: Alpha, 13-16: Beta, 17-20: Gamma
    sensors = ['TP9', 'AF7', 'AF8', 'TP10']
    
    # Helper to get mean of 4 sensors
    def get_band_mean(df, start_col):
        return df.iloc[:, start_col:start_col+4].mean(axis=1)
    
    # Columns are 0-indexed. 
    # Delta starts at 1. Theta at 5. Alpha at 9. Beta at 13. Gamma at 17.
    theta = get_band_mean(df, 5)
    beta = get_band_mean(df, 13)
    gamma = get_band_mean(df, 17)
    
    # Create a clean dataframe
    clean_df = pd.DataFrame({
        'Timestamp': pd.to_datetime(df.iloc[:, 0]),
        'Theta': theta,
        'Beta': beta,
        'Gamma': gamma
    })
    
    # Smooth the data (rolling average) to reduce jitter for simulation
    clean_df['Theta'] = clean_df['Theta'].rolling(window=5).mean().fillna(0)
    clean_df['Beta'] = clean_df['Beta'].rolling(window=5).mean().fillna(0)
    clean_df['Gamma'] = clean_df['Gamma'].rolling(window=5).mean().fillna(0)
    
    return clean_df

# --- MAIN SIMULATION LOOP ---
def run_simulation():
    print("Loading EEG Data...")
    data = load_eeg_data('/home/ubuntu/upload/mindMonitor_2026-01-18--21-22-32.csv')
    
    print(f"Initializing Swarm with {len(data)} time steps...")
    swarm = CognitiveSwarm(num_agents=200)
    
    results = {
        'time': [],
        'swarm_entropy': [],
        'swarm_coherence': [],
        'gamma_input': [],
        'beta_input': []
    }
    
    # We will simulate every 10th frame to speed up processing
    step_size = 10
    
    for i in range(0, len(data), step_size):
        row = data.iloc[i]
        
        # Inject EEG into Swarm
        swarm.update(gamma=row['Gamma'], beta=row['Beta'], theta=row['Theta'])
        
        # Record State
        results['time'].append(i)
        results['swarm_entropy'].append(swarm.entropy)
        results['swarm_coherence'].append(swarm.coherence)
        results['gamma_input'].append(row['Gamma'])
        results['beta_input'].append(row['Beta'])
        
        if i % 1000 == 0:
            print(f"Simulating step {i}/{len(data)}")
            
    return results

# --- VISUALIZATION ---
def plot_results(results):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Plot 1: Brain Inputs
    ax1.set_title('Input: Neural Drivers (Gamma & Beta)')
    ax1.plot(results['time'], results['gamma_input'], color='magenta', label='Gamma (Insight/Speed)', alpha=0.8)
    ax1.plot(results['time'], results['beta_input'], color='cyan', label='Beta (Focus/Coupling)', alpha=0.8)
    ax1.legend()
    ax1.set_ylabel('Brainwave Power')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Swarm Response
    ax2.set_title('Output: Swarm Dynamics (Entropy & Coherence)')
    
    # Dual axis for Entropy and Coherence
    ax2_entropy = ax2
    ax2_coherence = ax2.twinx()
    
    ln1 = ax2_entropy.plot(results['time'], results['swarm_entropy'], color='orange', label='Swarm Entropy (Chaos)', linewidth=2)
    ln2 = ax2_coherence.plot(results['time'], results['swarm_coherence'], color='lime', label='Swarm Coherence (Order)', linewidth=2, linestyle='--')
    
    ax2_entropy.set_ylabel('Entropy', color='orange')
    ax2_coherence.set_ylabel('Coherence', color='lime')
    ax2.set_xlabel('Simulation Steps')
    
    # Combined Legend
    lns = ln1 + ln2
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc='upper left')
    
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/swarm_eeg_simulation.png')
    print("Simulation plot saved to swarm_eeg_simulation.png")

if __name__ == "__main__":
    res = run_simulation()
    plot_results(res)
