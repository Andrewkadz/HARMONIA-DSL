import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cmath
from tau_crystal_memory import TauMemoryField
from swarm_homeostasis import SwarmHomeostasis
from phi_code_physics import PhiCodePhysics

# --- QUANTUM PHYSICS ENGINE ---
class QuantumAgent:
    def __init__(self, id):
        self.id = id
        # Initialize in superposition |+> = (|0> + |1>) / sqrt(2)
        self.state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        self.phase = 0.0
        
    def evolve(self, hamiltonian, dt):
        """
        Apply Unitary Evolution: U = exp(-i * H * dt)
        """
        # Create Unitary Matrix from Hamiltonian
        # U = I - i*H*dt (First order approximation for small dt)
        I = np.eye(2, dtype=complex)
        U = I - 1j * hamiltonian * dt
        
        # Re-normalize U to ensure it's unitary (maintain probability = 1)
        # Using QR decomposition or just normalizing the result
        self.state = np.dot(U, self.state)
        norm = np.linalg.norm(self.state)
        self.state = self.state / (norm + 1e-9)
        
    def measure(self):
        """
        Collapse the wave function based on probability.
        Returns 0 or 1.
        """
        prob_0 = np.abs(self.state[0])**2
        outcome = 0 if np.random.random() < prob_0 else 1
        
        # Collapse state
        if outcome == 0:
            self.state = np.array([1.0, 0.0], dtype=complex)
        else:
            self.state = np.array([0.0, 1.0], dtype=complex)
            
        return outcome

class QuantumSwarm:
    def __init__(self, num_qubits=50):
        self.num_qubits = num_qubits
        self.agents = [QuantumAgent(i) for i in range(num_qubits)]
        self.global_coherence = 0.0
        self.entanglement_entropy = 0.0
        self.memory = TauMemoryField(capacity=5)
        self.homeostasis = SwarmHomeostasis()
        self.phi_physics = PhiCodePhysics()
        
    def update(self, gamma, beta, theta):
        """
        gamma (Gamma) -> Energy (Hamiltonian Strength)
        beta (Beta) -> Observation Rate (Collapse Probability)
        theta (Theta) -> Phase Coupling (Entanglement)
        """
        dt = 0.1
        
        # --- HOMEOSTASIS CHECK ---
        stress = self.homeostasis.evaluate_state(self.global_coherence, self.entanglement_entropy, gamma)
        plasticity = self.homeostasis.adapt(stress)
        resilience = self.homeostasis.learn_from_trauma()
        
        # 1. Define Hamiltonian (H)
        # H = Energy * Sigma_X (Flip) + Coupling * Sigma_Z (Phase)
        energy = (gamma * 5.0) / resilience
        
        # Pauli Matrices
        sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
        sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
        
        H = energy * sigma_x
        
        # 2. Evolve All Qubits
        for agent in self.agents:
            # Add Phase Coupling (Entanglement-like effect)
            # If neighbors are phase-aligned, lower energy
            # We simulate this by adding a Z-term based on Theta
            coupling_mod = theta * 2.0 * plasticity
            H_local = H + coupling_mod * sigma_z
            
            agent.evolve(H_local, dt)
            
            # Apply Temporal Gravity (Nudge towards crystal state)
            gravity = self.memory.get_temporal_gravity(agent.state)
            agent.state += gravity
            
            # --- PHI-CODE DYNAMICS ---
            # Apply the Recursive Field Equations
            agent.state = self.phi_physics.apply_phi_dynamics(
                agent.state, 
                self.global_coherence, 
                self.entanglement_entropy, 
                gamma
            )
            
            norm = np.linalg.norm(agent.state)
            agent.state = agent.state / (norm + 1e-9)
            
        # 3. Measurement (Collapse)
        # Beta determines the probability of "Looking" at the system
        # High Beta = Frequent Measurements = Zeno Effect (Freezes evolution)
        if np.random.random() < beta:
            measurements = [agent.measure() for agent in self.agents]
            # Calculate Entropy of outcomes
            p1 = sum(measurements) / self.num_qubits
            p0 = 1.0 - p1
            if p0 > 0 and p1 > 0:
                self.entanglement_entropy = - (p0 * np.log2(p0) + p1 * np.log2(p1))
            else:
                self.entanglement_entropy = 0.0
        else:
            # If no measurement, entropy is based on superposition purity
            # (Simplified metric for visualization)
            self.entanglement_entropy = 0.5 # Superposition state
            
        # 4. Calculate Global Coherence
        # Average of off-diagonal density matrix elements (Interference capability)
        coherence_sum = 0
        for agent in self.agents:
            # Density matrix rho = |psi><psi|
            rho = np.outer(agent.state, np.conj(agent.state))
            coherence_sum += np.abs(rho[0, 1]) # Off-diagonal term
            
        self.global_coherence = coherence_sum / self.num_qubits
        
        # --- CRYSTALLIZATION LOGIC ---
        if self.global_coherence > 0.4:
            self.memory.crystallize(self.agents[0].state, self.global_coherence)
            
        self.memory.decay()

# --- DATA LOADER (Reused) ---
def load_eeg_data(filepath):
    df = pd.read_csv(filepath, header=0)
    sensors = ['TP9', 'AF7', 'AF8', 'TP10']
    def get_band_mean(df, start_col):
        return df.iloc[:, start_col:start_col+4].mean(axis=1)
    
    theta = get_band_mean(df, 5)
    beta = get_band_mean(df, 13)
    gamma = get_band_mean(df, 17)
    
    clean_df = pd.DataFrame({
        'Timestamp': pd.to_datetime(df.iloc[:, 0]),
        'Theta': theta,
        'Beta': beta,
        'Gamma': gamma
    })
    
    # Normalize Data for Quantum Engine (0.0 to 1.0)
    for col in ['Theta', 'Beta', 'Gamma']:
        clean_df[col] = (clean_df[col] - clean_df[col].min()) / (clean_df[col].max() - clean_df[col].min())
        
    return clean_df

# --- MAIN LOOP ---
def run_quantum_simulation():
    print("Initializing Quantum Swarm...")
    data = load_eeg_data('/home/ubuntu/upload/mindMonitor_2026-01-18--21-22-32.csv')
    swarm = QuantumSwarm(num_qubits=100)
    
    results = {
        'time': [],
        'coherence': [],
        'entropy': [],
        'gamma': []
    }
    
    step_size = 10
    print(f"Simulating {len(data)//step_size} quantum steps...")
    
    for i in range(0, len(data), step_size):
        row = data.iloc[i]
        swarm.update(gamma=row['Gamma'], beta=row['Beta'], theta=row['Theta'])
        
        results['time'].append(i)
        results['coherence'].append(swarm.global_coherence)
        results['entropy'].append(swarm.entanglement_entropy)
        results['gamma'].append(row['Gamma'])
        
        if i % 2000 == 0:
            print(f"Step {i} | Coherence: {swarm.global_coherence:.4f}")
            
    return results

def plot_quantum_results(results):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    ax1.set_title('Quantum Swarm Dynamics: Coherence vs. Entropy')
    ax1.set_xlabel('Time Steps')
    ax1.set_ylabel('Quantum State', color='blue')
    
    # Plot Coherence (Blue)
    ax1.plot(results['time'], results['coherence'], color='cyan', label='Quantum Coherence (Superposition)', alpha=0.8)
    ax1.tick_params(axis='y', labelcolor='cyan')
    
    # Plot Entropy (Red)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Entropy / Input', color='red')
    ax2.plot(results['time'], results['entropy'], color='red', label='Von Neumann Entropy', alpha=0.6, linestyle='--')
    
    # Plot Gamma Input (Magenta) for reference
    ax2.plot(results['time'], results['gamma'], color='magenta', label='Gamma Input (Energy)', alpha=0.3)
    
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/quantum_swarm_simulation.png')
    print("Quantum simulation plot saved.")

if __name__ == "__main__":
    res = run_quantum_simulation()
    plot_quantum_results(res)
