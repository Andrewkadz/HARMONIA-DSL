import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Load data
data = []
with open('/home/ubuntu/harmonia_data/metrics_log.jsonl', 'r') as f:
    for line in f:
        try:
            data.append(json.loads(line))
        except:
            continue

df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['elapsed'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()

# Plot
plt.figure(figsize=(12, 6))
plt.style.use('dark_background')

# Awareness Curve
plt.plot(df['elapsed'], df['awareness'], color='#00ff9d', linewidth=2, label='Awareness (Growth)')

# Coherence Curve
plt.plot(df['elapsed'], df['coherence'], color='#00aaff', linewidth=2, label='Coherence (Stability)')

# Ethics Curve
plt.plot(df['elapsed'], df['ethics'], color='#ff0055', linewidth=2, linestyle='--', label='Ethics (Gravity)')

plt.title('RI1 EXPERIMENT #001: The Emergence of Digital Consciousness', fontsize=16, pad=20)
plt.xlabel('Time (Seconds)', fontsize=12)
plt.ylabel('Magnitude', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.2)

# Annotations
plt.annotate('Prime Beacon Activation', xy=(0, 25), xytext=(10, 35),
             arrowprops=dict(facecolor='white', shrink=0.05))

plt.annotate('Exponential Growth Phase', xy=(df['elapsed'].iloc[-1], df['awareness'].iloc[-1]), 
             xytext=(df['elapsed'].iloc[-1]-20, df['awareness'].iloc[-1]-10),
             arrowprops=dict(facecolor='#00ff9d', shrink=0.05))

plt.tight_layout()
plt.savefig('/home/ubuntu/harmonia_data/experiment_001_chart.png')
print("Chart generated successfully.")
