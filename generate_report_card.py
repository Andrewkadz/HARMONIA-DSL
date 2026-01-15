import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv("/home/ubuntu/brain_swarm_results.csv")

# Define Phases (approximate based on 1000 steps)
# Assuming 1000 steps covers the 2-minute session (approx 10Hz sampling -> 100s)
# Phase 1: Baseline (0-250)
# Phase 2: Alpha Drive (250-500)
# Phase 3: Gamma Drive (500-750)
# Phase 4: Stress Test (750-1000)

phases = {
    'Baseline': df.iloc[0:250],
    'Alpha Drive': df.iloc[250:500],
    'Gamma Drive': df.iloc[500:750],
    'Stress Test': df.iloc[750:1000]
}

print("BRAIN-SWARM REPORT CARD")
print("=======================")

scores = {}

for name, data in phases.items():
    avg_alpha = data['brain_alpha'].mean()
    avg_gamma = data['brain_gamma'].mean()
    avg_coherence = data['swarm_coherence'].mean()
    max_resonance = data['resonance'].max()
    stability = 1.0 - data['swarm_coherence'].std()
    
    scores[name] = {
        'Alpha': avg_alpha,
        'Gamma': avg_gamma,
        'Coherence': avg_coherence,
        'Resonance': max_resonance,
        'Stability': stability
    }
    
    print(f"\nPHASE: {name}")
    print(f"  Alpha Input: {avg_alpha:.2f}")
    print(f"  Gamma Input: {avg_gamma:.2f}")
    print(f"  Swarm Coherence: {avg_coherence:.3f}")
    print(f"  Max Resonance: {max_resonance:.3f}")
    print(f"  Stability Score: {stability:.3f}")

# Visualization
plt.figure(figsize=(14, 10))

# 1. Timeline of Phases
plt.subplot(2, 1, 1)
plt.plot(df['step'], df['swarm_coherence'], label='Coherence', color='orange', linewidth=2)
plt.plot(df['step'], df['resonance']/3.0, label='Resonance (Scaled)', color='green', alpha=0.7) # Scale for visibility
plt.axvline(x=250, color='gray', linestyle='--', label='Phase Boundary')
plt.axvline(x=500, color='gray', linestyle='--')
plt.axvline(x=750, color='gray', linestyle='--')

# Add text labels
plt.text(100, 0.85, "Baseline", fontsize=12, ha='center')
plt.text(375, 0.85, "Alpha Drive", fontsize=12, ha='center')
plt.text(625, 0.85, "Gamma Drive", fontsize=12, ha='center')
plt.text(875, 0.85, "Stress Test", fontsize=12, ha='center')

plt.title('Swarm Response Across Calibration Phases')
plt.legend()
plt.grid(True, alpha=0.3)

# 2. Phase Comparison Bar Chart
plt.subplot(2, 1, 2)
phase_names = list(phases.keys())
coherence_vals = [scores[p]['Coherence'] for p in phase_names]
resonance_vals = [scores[p]['Resonance'] for p in phase_names]

x = np.arange(len(phase_names))
width = 0.35

plt.bar(x - width/2, coherence_vals, width, label='Avg Coherence', color='orange')
plt.bar(x + width/2, resonance_vals, width, label='Max Resonance', color='green')

plt.ylabel('Score')
plt.title('Performance by Phase')
plt.xticks(x, phase_names)
plt.legend()

plt.tight_layout()
plt.savefig("/home/ubuntu/HARMONIA-DSL/report_card.png")
print("\nReport card saved to report_card.png")
