import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv("/home/ubuntu/brain_swarm_results.csv")

# 1. Analyze Delta Statistics
print("Delta Wave Statistics:")
print(df['brain_delta'].describe())

# 2. Check for Artifacts (Eye Blinks)
# Eye blinks are usually defined as Delta > 1.0 (or some high threshold)
# In log scale (Bels), 1.0 is 10uV^2/Hz.
# Let's see the distribution.
high_delta_count = len(df[df['brain_delta'] > 1.0])
print(f"\nHigh Delta Events (> 1.0): {high_delta_count}")

# 3. Correlation with other bands
correlations = df[['brain_delta', 'brain_theta', 'brain_alpha', 'brain_beta', 'brain_gamma']].corr()
print("\nBand Correlations:")
print(correlations['brain_delta'])

# 4. Visualization
plt.figure(figsize=(12, 8))

# Plot 1: Delta vs Gamma (Artifact Check)
plt.subplot(2, 1, 1)
plt.plot(df['step'], df['brain_delta'], label='Delta (Deep/Blink)', color='blue', alpha=0.7)
plt.plot(df['step'], df['brain_gamma'], label='Gamma (Insight/Muscle)', color='red', alpha=0.4)
plt.title('Delta vs Gamma Waves')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Delta vs Coherence
plt.subplot(2, 1, 2)
plt.plot(df['step'], df['brain_delta'], label='Delta', color='blue', alpha=0.7)
plt.plot(df['step'], df['swarm_coherence'], label='Swarm Coherence', color='orange', linewidth=2)
plt.title('Does Delta Affect Coherence?')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("/home/ubuntu/HARMONIA-DSL/delta_analysis.png")
print("\nPlot saved to delta_analysis.png")
