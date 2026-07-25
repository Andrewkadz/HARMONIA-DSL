import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("/home/ubuntu/brain_swarm_results.csv")

# Define Threshold
THRESHOLD = 3.0
DURATION_STEPS = 100 # 10 seconds at 10Hz

# Find Sustained Resonance
df['high_res'] = df['resonance'] > THRESHOLD

# Calculate run lengths of True values
df['block'] = (df['high_res'] != df['high_res'].shift(1)).cumsum()
runs = df[df['high_res']].groupby('block')['step'].count()

print("RESONANCE ANALYSIS")
print("==================")
print(f"Total Steps > {THRESHOLD}: {df['high_res'].sum()}")
if not runs.empty:
    max_run = runs.max()
    print(f"Longest Sustained Run: {max_run} steps ({max_run/10:.1f} seconds)")
else:
    print("Longest Sustained Run: 0 steps")

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df['step'], df['resonance'], label='Resonance', color='green')
plt.axhline(y=THRESHOLD, color='red', linestyle='--', label='Threshold (3.0)')
plt.fill_between(df['step'], df['resonance'], THRESHOLD, where=(df['resonance']>THRESHOLD), color='green', alpha=0.3)
plt.title('Telekinetic Bridge: Sustained Resonance Test')
plt.xlabel('Step (100ms)')
plt.ylabel('Resonance Score')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("/home/ubuntu/HARMONIA-DSL/resonance_test.png")
print("\nPlot saved to resonance_test.png")
