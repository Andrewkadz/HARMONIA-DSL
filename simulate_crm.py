import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Load the Matrix ---
def load_hrm(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    topology_lines = []
    reading_topology = False
    for line in lines:
        if "[TOPOLOGY]" in line:
            reading_topology = True
            continue
        if "[PROPERTIES]" in line:
            break
        if reading_topology and line.strip():
            topology_lines.append(line.strip().split())
            
    return np.array(topology_lines)

# --- 2. Define Physics Rules (The "Code") ---
# Each glyph modifies the energy passing through it
GLYPH_RULES = {
    'Θ': 1.0,   # Loop: Maintains energy (Identity)
    'π': 1.0,   # Cycle: Maintains energy
    'Ω': 0.1,   # Termination: Absorbs/Dampens energy (Resistance)
    'Φ': 1.618, # Phi: Amplifies energy (Gain)
    'Δ': 0.8,   # Delta: Tension (Slight loss due to friction)
    'Σ': 1.2,   # Sigma: Summation (Accumulates)
    'Λ': 2.0,   # Lambda: Shift (Massive boost/instability)
    'Ψ': 1.0,   # Psi: Wave (Transmits perfectly)
    'Γ': 1.0,   # Gamma: Connection (Transmits)
    'Xi': 1.0,  # Field (Background)
    'λ': 0.5,   # Lowercase Lambda: Decay
    'O': 0.0,   # Void: Blocks energy
    'ρ': 0.9,   # Rho: Density (Slight damping)
    'τ': 1.0,   # Tau: Time (Flow)
}

def get_glyph_factor(glyph):
    return GLYPH_RULES.get(glyph, 1.0) # Default to 1.0 if unknown

# --- 3. The Resonance Engine ---
def run_simulation(matrix, steps=50):
    rows, cols = matrix.shape
    # Energy Grid (Float)
    energy = np.zeros((rows, cols))
    
    # Inject Lambda Pulse at Center
    center_r, center_c = rows // 2, cols // 2
    energy[center_r, center_c] = 100.0 # Massive Injection
    
    history = [energy.copy()]
    
    for t in range(steps):
        new_energy = np.zeros_like(energy)
        
        for r in range(rows):
            for c in range(cols):
                # Current Glyph
                glyph = matrix[r, c]
                factor = get_glyph_factor(glyph)
                
                # Diffusion: Energy flows to neighbors
                # We use a simple 4-neighbor diffusion model
                neighbors = []
                if r > 0: neighbors.append((r-1, c))
                if r < rows-1: neighbors.append((r+1, c))
                if c > 0: neighbors.append((r, c-1))
                if c < cols-1: neighbors.append((r, c+1))
                
                # Calculate incoming energy from neighbors
                incoming = 0
                for nr, nc in neighbors:
                    # Neighbor gives 20% of its energy to this cell
                    incoming += energy[nr, nc] * 0.20 
                
                # Apply Glyph Rule (Amplification/Damping)
                # The cell's new energy is (Retained Energy + Incoming) * Factor
                # Retained = 20% (it gave away 80% to 4 neighbors)
                retained = energy[r, c] * 0.20
                
                new_energy[r, c] = (retained + incoming) * factor
                
                # Cap energy to prevent infinite explosion (Saturation)
                if new_energy[r, c] > 1000:
                    new_energy[r, c] = 1000
                    
        energy = new_energy
        history.append(energy.copy())
        
    return history

# --- 4. Visualization ---
def visualize_results(history, matrix):
    # Plot Initial, Middle, and Final State
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    times = [0, 10, 49] # T=0, T=10, T=50
    titles = ["Injection (T=0)", "Propagation (T=10)", "Steady State (T=50)"]
    
    for i, t in enumerate(times):
        sns.heatmap(history[t], ax=axes[i], cmap="magma", cbar=False, square=True)
        axes[i].set_title(titles[i])
        axes[i].axis('off')
        
    plt.suptitle("CRM Simulation: Lambda Injection Response", fontsize=16)
    plt.savefig('/home/ubuntu/crm_simulation_results.png')
    plt.close()

if __name__ == "__main__":
    # Load the digitized matrix
    matrix = load_hrm('/home/ubuntu/HARMONIA-DSL/CRM_NODE_32.hrm')
    
    # Run Simulation
    history = run_simulation(matrix, steps=50)
    
    # Visualize
    visualize_results(history, matrix)
    print("Simulation Complete. Results saved to crm_simulation_results.png")
