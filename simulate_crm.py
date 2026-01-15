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

# --- 3. The Resonance Engine (Equation Driven) ---
def run_simulation(matrix, steps=135):
    rows, cols = matrix.shape
    # Energy Grid (Float)
    energy = np.zeros((rows, cols))
    
    # Inject Lambda Pulse at Center
    center_r, center_c = rows // 2, cols // 2
    energy[center_r, center_c] = 100.0 # Massive Injection
    
    history = [energy.copy()]
    
    # Constants for the Equation
    GLOBAL_CONST = 2.71134 # (263/97) - Phi-Pi-Epsilon
    TIME_CONST = 1.0       # T
    DECAY_CONST = 0.5      # lambda
    EPSILON = 1e-6         # To avoid division by zero
    
    for t in range(steps):
        new_energy = np.zeros_like(energy)
        
        for r in range(rows):
            for c in range(cols):
                # Current Glyph Factors
                glyph = matrix[r, c]
                shift_factor = get_glyph_factor(glyph) # Lambda (Local Shift)
                damping_factor = 0.5 # Omega (Local Damping - simplified)
                if glyph == 'Ω': damping_factor = 2.0 # Strong damping for Omega
                
                # 1. Calculate Flux (Gamma * P / T)
                # Sum of incoming energy from neighbors
                neighbors = []
                if r > 0: neighbors.append((r-1, c))
                if r < rows-1: neighbors.append((r+1, c))
                if c > 0: neighbors.append((r, c-1))
                if c < cols-1: neighbors.append((r, c+1))
                
                incoming_flux = 0
                for nr, nc in neighbors:
                    incoming_flux += energy[nr, nc] * 0.25 # Gamma (Connection)
                
                # 2. The Equation: Φπε · [ΓΛ(P/T) : ΨΩ] · Θn(P/λ)
                # Term 1: Global Context
                term1 = GLOBAL_CONST
                
                # Term 2: The Engine [Flux : State]
                # Numerator: Gamma * Lambda * (P_incoming / T)
                numerator = incoming_flux * shift_factor / TIME_CONST
                
                # Denominator: Psi * Omega (Current State * Damping)
                current_state = energy[r, c]
                denominator = (current_state * damping_factor) + EPSILON
                
                # Term 3: The Clock (Recursion)
                # P / lambda
                term3 = current_state / DECAY_CONST
                
                # Revised Logic for Stability:
                # New_Energy = (Incoming Flux * Shift) + (Retained Energy * Decay_Inverse)
                # But modulated by the "Ratio" [Flux : State]
                
                ratio = numerator / (current_state + 1.0) # Avoid div/0
                
                # Apply the Global Constant as a "Gain" on the Ratio
                update_force = term1 * ratio
                
                # Apply Recursion: The previous state persists but decays
                recursion = current_state * 0.8 # Natural decay
                
                new_val = recursion + update_force
                
                # Cap energy
                if new_val > 1000: new_val = 1000
                
                new_energy[r, c] = new_val
                    
        energy = new_energy
        history.append(energy.copy())
        
    return history

# --- 4. Visualization ---
def visualize_results(history, matrix):
    # Plot Initial, Middle, and Final State
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    times = [1, 73, 134] # Step 1, Step 73, Step 134
    titles = ["Reaction (T=1)", "Midpoint (T=73)", "Result (T=134)"]
    
    for i, t in enumerate(times):
        sns.heatmap(history[t], ax=axes[i], cmap="magma", cbar=False, square=True)
        axes[i].set_title(titles[i])
        axes[i].axis('off')
        
    plt.suptitle("CRM Simulation: Equation Driven (Phi-Pi-Epsilon)", fontsize=16)
    plt.savefig('/home/ubuntu/HARMONIA-DSL/crm_snapshots_1_73_134.png')
    plt.close()

if __name__ == "__main__":
    # Load the digitized matrix
    matrix = load_hrm('/home/ubuntu/HARMONIA-DSL/CRM_NODE_32.hrm')
    
    # Run Simulation
    history = run_simulation(matrix, steps=135)
    
    # Visualize
    visualize_results(history, matrix)
    print("Simulation Complete. Results saved to crm_snapshots_1_73_134.png")
