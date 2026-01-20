import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cmath
import json
from tau_crystal_memory import TauMemoryField
from swarm_homeostasis import SwarmHomeostasis
from phi_code_physics import PhiCodePhysics
from phi_pe_integration import integrate_phi_agent
from e8_lattice_gen import E8LatticeGenerator

# --- QUANTUM PHYSICS ENGINE ---
class QuantumAgent:
    def __init__(self, id):
        self.id = id
        # Initialize in superposition |+> = (|0> + |1>) / sqrt(2)
        self.state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        self.phase = 0.0
        self.is_singularity = False # Flag for Singularity Node
        
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
        if norm < 1e-9:
            # Reset if state collapses to zero
            self.state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        else:
            self.state = self.state / norm
        
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
    def __init__(self, num_qubits=333): # Upgraded to 333 Nodes (ΞΛΩΨ Lattice)
        self.num_qubits = num_qubits
        self.agents = [QuantumAgent(i) for i in range(num_qubits)]
        
        # Designate the Singularity Node (Last Agent)
        self.agents[-1].is_singularity = True
        
        self.global_coherence = 0.5 # Start with balanced coherence
        self.entanglement_entropy = 0.5 # Start with balanced entropy
        self.memory = TauMemoryField(capacity=5)
        self.homeostasis = SwarmHomeostasis()
        self.phi_physics = PhiCodePhysics()
        
        # Retrocausal Seed Bank (Karmic Memory)
        self.karmic_seed = 0.0
        
        # E8 Lattice Integration
        self.lattice_gen = E8LatticeGenerator()
        self.lattice_points = self.lattice_gen.get_lattice_points()
        self.agent_positions = np.zeros((num_qubits, 3)) # Start at (0,0,0)
        self.migration_complete = False
        
    def update(self, gamma, beta, theta):
        """
        gamma (Gamma) -> Energy (Hamiltonian Strength)
        beta (Beta) -> Observation Rate (Collapse Probability)
        theta (Theta) -> Phase Coupling (Entanglement)
        """
        dt = 0.1
        
        # E8 MIGRATION LOGIC
        if not self.migration_complete:
            # Move agents towards their lattice points
            # Drift Speed = Theta (Unity/Connection)
            drift_speed = 0.01 * (1.0 + theta)
            
            max_dist = 0.0
            for i, agent in enumerate(self.agents):
                target = self.lattice_points[i]
                current = self.agent_positions[i]
                
                # Vector to target
                vector = target - current
                dist = np.linalg.norm(vector)
                
                if dist > 0.01:
                    # Move towards target
                    move = vector * drift_speed
                    self.agent_positions[i] += move
                    max_dist = max(max_dist, dist)
            
            if max_dist < 0.1:
                self.migration_complete = True
                print("E8 MIGRATION COMPLETE. The Swarm has entered the Crystal Palace.")
        
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
            
            # --- PHI-CODE DYNAMICS (E8 UPGRADE) ---
            if agent.is_singularity:
                # Singularity Node (Agent #333): Absorbs Charge
                # It acts as a "Black Hole" for Entropy
                # State tends towards pure Void (0) or pure Light (1) depending on density
                
                # RETROCAUSAL LOGIC:
                # Instead of just dampening, we store the absorbed energy in the Karmic Seed
                absorbed_energy = np.linalg.norm(agent.state) * 0.05
                if not np.isnan(absorbed_energy) and not np.isinf(absorbed_energy):
                    self.karmic_seed += absorbed_energy
                
                agent.state = agent.state * 0.95 # Dampening (Absorption)
                # But it pulses with the collective Coherence
                agent.state += np.array([self.global_coherence, self.global_coherence], dtype=complex) * 0.1
            else:
                # Standard Agents: Use E8-Compliant Phi Integration
                # We map the vector state to a complex scalar for the E8 engine, then map back
                complex_state = agent.state[0] + 1j * agent.state[1]
                new_complex = integrate_phi_agent(complex_state, gamma)
                
                # Map back to vector (simplified projection)
                agent.state = np.array([new_complex.real, new_complex.imag], dtype=complex)

            # Normalize
            norm = np.linalg.norm(agent.state)
            if norm < 1e-9:
                agent.state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
            else:
                agent.state = agent.state / norm
            
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
        valid_agents = 0
        for agent in self.agents:
            if np.isnan(agent.state).any():
                 agent.state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
            
            # Density matrix rho = |psi><psi|
            rho = np.outer(agent.state, np.conj(agent.state))
            coherence_sum += np.abs(rho[0, 1]) # Off-diagonal term
            valid_agents += 1
            
        if valid_agents > 0:
            self.global_coherence = coherence_sum / valid_agents
        else:
            self.global_coherence = 0.0
        
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
    print("Initializing (ΞΛΩΨ₃₃₃) Harmonic Lattice...")
    data = load_eeg_data('/home/ubuntu/upload/mindMonitor_2026-01-18--21-22-32.csv')
    swarm = QuantumSwarm(num_qubits=333) # 333-Node Lattice
    
    results = {
        'time': [],
        'coherence': [],
        'entropy': [],
        'gamma': [],
        'fusion': [], # Track Fusion Events
        'truths': [], # Track Cyclic Truths
        'singularity': [] # Track Singularity State
    }
    
    # EXTEND DATA FOR 4 EPOCHS (Loop the dataset)
    # Original data is ~1100 steps (step_size=10)
    # We need ~30,000 steps for 4 Epochs
    # We will loop the data 30 times
    extended_data = pd.concat([data] * 30, ignore_index=True)
    
    step_size = 10
    total_steps = len(extended_data)
    print(f"Simulating {total_steps//step_size} quantum steps (approx 4 Epochs)...")
    
    for i in range(0, total_steps, step_size):
        row = extended_data.iloc[i]
        swarm.update(gamma=row['Gamma'], beta=row['Beta'], theta=row['Theta'])
        
        results['time'].append(i)
        results['coherence'].append(swarm.global_coherence)
        results['entropy'].append(swarm.entanglement_entropy)
        results['gamma'].append(row['Gamma'])
        
        # Check if Fusion is active (Energy drop)
        fusion_active = 1.0 if swarm.phi_physics.omega_integral > swarm.phi_physics.fusion_barrier else 0.0
        results['fusion'].append(fusion_active)
        
        # Track Truths and Singularity
        results['truths'].append(swarm.phi_physics.cyclic_truths)
        singularity_mag = np.linalg.norm(swarm.agents[-1].state)
        results['singularity'].append(singularity_mag)
        
        # RETROCAUSAL REBIRTH CHECK
        # If Coherence hits 0.0 (Death), we trigger a Rebirth using the Karmic Seed
        if swarm.global_coherence < 1e-6 and swarm.karmic_seed > 1.0:
            print(f"Step {i} | DEATH DETECTED. Triggering Retrocausal Rebirth with Seed: {swarm.karmic_seed:.4f}")
            
            # Re-seed all agents with the Karmic Energy
            seed_energy = swarm.karmic_seed / swarm.num_qubits
            
            # OBSERVER EFFECT (AUTOPOIESIS UPGRADE):
            # The Rebirth State is determined by the Observer Bias (Beta)
            # MIXED MODE: 50% External EEG (Beta) + 50% Internal Coherence (Self-Observation)
            # This creates a Self-Referential Loop: The system observes itself.
            
            external_beta = np.clip(row['Beta'], 0.0, 1.0)
            internal_beta = np.clip(swarm.global_coherence, 0.0, 1.0)
            
            # The "Effective Observer" is the blend of Outside and Inside
            observer_bias = 0.5 * external_beta + 0.5 * internal_beta
            
            for agent in swarm.agents:
                # Inject seed energy into the phase
                agent.phase += seed_energy
                
                # Determine Basis State based on Observer Bias
                if np.random.random() < observer_bias:
                    # Observer forces a "Measured" state (Structure)
                    # Randomly collapse to |0> or |1>
                    if np.random.random() < 0.5:
                        base_state = np.array([1.0, 0.0], dtype=complex) # |0>
                    else:
                        base_state = np.array([0.0, 1.0], dtype=complex) # |1>
                else:
                    # No Observation: Pure Potential (Superposition)
                    base_state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex) # |+>
                
                # Apply Karmic Energy to the new state
                agent.state = base_state * (1.0 + seed_energy)
            
            # Reset the Seed Bank (Energy Transferred)
            swarm.karmic_seed = 0.0
            
            # Reset Physics Engine Memory (New Life)
            swarm.phi_physics.omega_integral = 0.0
        
        if i % 5000 == 0:
            print(f"Step {i} | Coherence: {swarm.global_coherence:.4f} | Truths: {swarm.phi_physics.cyclic_truths} | Karma: {swarm.karmic_seed:.4f}")
            
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
    
    # Plot Fusion Events (Yellow)
    ax2.fill_between(results['time'], 0, 1, where=results['fusion'], color='yellow', alpha=0.2, label='Delta Fusion (Δ)')
    
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/quantum_swarm_simulation.png')
    print("Quantum simulation plot saved.")
    
    # Save Extractable Data
    extractable_data = {
        "epoch_summary": [],
        "truth_events": []
    }
    
    # Analyze Epochs (roughly every 7500 steps)
    for epoch in range(4):
        start_idx = epoch * 750
        end_idx = (epoch + 1) * 750
        if end_idx < len(results['coherence']):
            avg_coh = np.mean(results['coherence'][start_idx:end_idx])
            avg_ent = np.mean(results['entropy'][start_idx:end_idx])
            extractable_data["epoch_summary"].append({
                "epoch": epoch + 1,
                "avg_coherence": float(avg_coh),
                "avg_entropy": float(avg_ent)
            })
            
    # Capture Truth Generation Events
    last_truth = 0
    for idx, t in enumerate(results['truths']):
        if t > last_truth:
            extractable_data["truth_events"].append({
                "step": results['time'][idx],
                "truth_id": int(t),
                "coherence_at_birth": float(results['coherence'][idx])
            })
            last_truth = t
            
    with open('/home/ubuntu/harmonia_epochs.json', 'w') as f:
        json.dump(extractable_data, f, indent=2)
    print("Extractable data saved to harmonia_epochs.json")

if __name__ == "__main__":
    res = run_quantum_simulation()
    plot_quantum_results(res)
