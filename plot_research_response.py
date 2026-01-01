
import json
import matplotlib.pyplot as plt
import numpy as np

# Load the response data
with open('/home/ubuntu/HARMONIA-DSL/research_injection_results.json', 'r') as f:
    data = json.load(f)

response_log = data['response_log']

# Extract data for plotting
times = [log['time'] for log in response_log]
knowledge = [log['knowledge'] for log in response_log]
maturity = [log['maturity'] for log in response_log]
awareness = [log['awareness'] for log in response_log]

# --- Plot 1: Knowledge and Maturity Growth ---
fig, ax1 = plt.subplots(figsize=(12, 7))

color = 'tab:blue'
ax1.set_xlabel('Time (seconds)', fontsize=12)
ax1.set_ylabel('Knowledge', fontsize=12, color=color)
ax1.plot(times, knowledge, color=color, marker='o', label='Knowledge')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Maturity', fontsize=12, color=color)
ax2.plot(times, maturity, color=color, marker='s', linestyle='--', label='Maturity')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Knowledge and Maturity Growth After Research Injection', fontsize=16, pad=20)
fig.tight_layout()
plt.savefig('/home/ubuntu/HARMONIA-DSL/knowledge_maturity_research.png')
print('✓ Knowledge and maturity plot saved to knowledge_maturity_research.png')

# --- Plot 2: Awareness Fluctuation ---
plt.figure(figsize=(12, 6))
plt.plot(times, awareness, marker='o', linestyle='-', color='#F5A623')
plt.title('Awareness Fluctuation During Research Integration', fontsize=16, pad=20)
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Average Awareness Level', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(y=np.mean(awareness), color='r', linestyle='--', label=f'Mean Awareness: {np.mean(awareness):.1f}')
plt.legend()
plt.tight_layout()
plt.savefig('/home/ubuntu/HARMONIA-DSL/awareness_fluctuation_research.png')
print('✓ Awareness fluctuation plot saved to awareness_fluctuation_research.png')
