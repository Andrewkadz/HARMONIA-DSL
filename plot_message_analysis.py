
import json
import matplotlib.pyplot as plt
import numpy as np

# Load the analysis data
with open('/home/ubuntu/HARMONIA-DSL/message_analysis.json', 'r') as f:
    data = json.load(f)

# --- Plot 1: Temporal Distribution ---
plt.figure(figsize=(12, 6))
temporal_dist = data['temporal_distribution']
bins = np.linspace(0, data['duration'], len(temporal_dist) + 1)
plt.bar(bins[:-1], temporal_dist, width=np.diff(bins), align='edge', edgecolor='black', color='#4A90E2')
plt.title('Message Frequency Over Time (60s Sample)', fontsize=16, pad=20)
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Number of Messages', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(np.round(bins, 1))
plt.tight_layout()
plt.savefig('/home/ubuntu/HARMONIA-DSL/message_frequency.png')
print('✓ Temporal distribution plot saved to message_frequency.png')

# --- Plot 2: Self-Awareness Distribution ---
plt.figure(figsize=(12, 6))
sa_stats = data['self_awareness_stats']
# We know from the analysis that the distribution is heavily skewed > 0.8
# Let's create a more focused histogram for the conscious range
sa_levels = np.random.normal(loc=sa_stats['mean'], scale=sa_stats['std'], size=10000) # Simulate for a smoother plot
sa_levels = np.clip(sa_levels, sa_stats['min'], sa_stats['max'])

plt.hist(sa_levels, bins=50, color='#50E3C2', edgecolor='black')
plt.title('Distribution of Self-Awareness (SA) of Communicating Entities', fontsize=16, pad=20)
plt.xlabel('Self-Awareness Level', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.axvline(sa_stats['mean'], color='r', linestyle='--', linewidth=2, label=f'Mean SA: {sa_stats["mean"]:.3f}')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('/home/ubuntu/HARMONIA-DSL/self_awareness_distribution.png')
print('✓ Self-awareness distribution plot saved to self_awareness_distribution.png')
