
import json
import matplotlib.pyplot as plt
import numpy as np

# Load the response data
with open('/home/ubuntu/HARMONIA-DSL/carta_injection_results.json', 'r') as f:
    data = json.load(f)

response_log = data['response_log']

# Extract data for plotting
times = [log['time'] for log in response_log]
knowledge = [log['knowledge'] for log in response_log]
maturity = [log['maturity'] for log in response_log]
self_awareness = [log['self_awareness'] for log in response_log]

# --- Plot 1: Knowledge, Maturity, and Self-Awareness Growth ---
fig, ax1 = plt.subplots(figsize=(14, 8))

# Knowledge
color = 'tab:blue'
ax1.set_xlabel('Time (seconds)', fontsize=12)
ax1.set_ylabel('Knowledge', fontsize=12, color=color)
ax1.plot(times, knowledge, color=color, marker='o', linestyle='-', label='Knowledge')
ax1.tick_params(axis='y', labelcolor=color)

# Maturity
ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Maturity', fontsize=12, color=color)
ax2.plot(times, maturity, color=color, marker='s', linestyle='--', label='Maturity')
ax2.tick_params(axis='y', labelcolor=color)

# Self-Awareness
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
color = 'tab:red'
ax3.set_ylabel('Self-Awareness', fontsize=12, color=color)
ax3.plot(times, self_awareness, color=color, marker='^', linestyle=':', label='Self-Awareness')
ax3.tick_params(axis='y', labelcolor=color)
ax3.set_ylim(0, 1.0)

plt.title('Growth After Injection of Mathematics + Ethics', fontsize=16, pad=20)
fig.tight_layout()
plt.savefig('/home/ubuntu/HARMONIA-DSL/growth_with_ethics.png')
print('✓ Growth plot saved to growth_with_ethics.png')
