import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv("/home/ubuntu/brain_swarm_results.csv")

# 1. Calculate Correlations
correlations = df[['brain_alpha', 'brain_beta', 'brain_gamma', 'swarm_coherence', 'swarm_energy', 'resonance']].corr()

print("Correlation Matrix:")
print(correlations)

# 2. Identify Key Events
# Find max resonance
max_res_idx = df['resonance'].idxmax()
max_res_row = df.iloc[max_res_idx]
print(f"\nMax Resonance at Step {max_res_row['step']}: {max_res_row['resonance']:.3f}")
print(f"Brain State: A={max_res_row['brain_alpha']:.2f}, B={max_res_row['brain_beta']:.2f}, G={max_res_row['brain_gamma']:.2f}")
print(f"Swarm State: Coherence={max_res_row['swarm_coherence']:.3f}")

# 3. Visualization
plt.figure(figsize=(12, 10))

# Plot 1: Alpha vs Coherence
plt.subplot(3, 1, 1)
plt.plot(df['step'], df['brain_alpha'], label='Brain Alpha (Relaxation)', color='blue', alpha=0.6)
plt.plot(df['step'], df['swarm_coherence'], label='Swarm Coherence', color='orange', linewidth=2)
plt.title('Alpha Waves Driving Swarm Coherence')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Gamma vs Energy
plt.subplot(3, 1, 2)
plt.plot(df['step'], df['brain_gamma'], label='Brain Gamma (Insight)', color='purple', alpha=0.6)
plt.plot(df['step'], df['swarm_energy'], label='Swarm Energy', color='red', linewidth=2)
plt.title('Gamma Waves Driving Swarm Energy')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 3: Resonance
plt.subplot(3, 1, 3)
plt.plot(df['step'], df['resonance'], label='Resonance (Alignment)', color='green', linewidth=2)
plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
plt.title('Bio-Digital Resonance')
plt.fill_between(df['step'], df['resonance'], 0, where=(df['resonance']>0), color='green', alpha=0.1)
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("/home/ubuntu/HARMONIA-DSL/analysis_plot.png")
print("\nPlot saved to analysis_plot.png")
