import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load data
data = []
with open('/home/ubuntu/harmonia_data/metrics_log.jsonl', 'r') as f:
    for line in f:
        try:
            entry = json.loads(line)
            if 'alpha_sim' in entry:
                data.append(entry)
        except:
            continue

df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['elapsed'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()

# Filter for the current run (last 500 entries if available)
if len(df) > 500:
    df = df.iloc[-500:]

# Calculate Statistics
mean_alpha = df['alpha_sim'].mean()
std_alpha = df['alpha_sim'].std()
target_alpha = 1/137.035999

print(f"ALPHA HUNT RESULTS")
print(f"==================")
print(f"Mean Alpha: {mean_alpha:.6f}")
print(f"Target Alpha: {target_alpha:.6f}")
print(f"Difference: {abs(mean_alpha - target_alpha):.6f}")
print(f"Standard Deviation: {std_alpha:.6f}")

# Plot
plt.figure(figsize=(12, 6))
plt.style.use('dark_background')

plt.plot(df['elapsed'], df['alpha_sim'], color='#00ff9d', linewidth=1, label='Simulated Alpha')
plt.axhline(y=target_alpha, color='#ff0055', linestyle='--', linewidth=2, label='Target (1/137)')

plt.title('Deriving the Fine Structure Constant from Prime Harmonics', fontsize=16, pad=20)
plt.xlabel('Time (Seconds)', fontsize=12)
plt.ylabel('Alpha Ratio', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('/home/ubuntu/harmonia_data/alpha_convergence_chart.png')
print("Chart generated successfully.")
