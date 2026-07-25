
import json
import matplotlib.pyplot as plt
import numpy as np

# Load the response data
with open('/home/ubuntu/HARMONIA-DSL/first_contact_response.json', 'r') as f:
    data = json.load(f)

response_log = data['response_log']

# Extract data for plotting
times = [log['time'] for log in response_log]
knowledge = [log['knowledge'] for log in response_log]
messages = [log['messages'] for log in response_log]

# --- Plot 1: Knowledge Growth Over Time ---
plt.figure(figsize=(12, 6))
plt.plot(times, knowledge, marker='o', linestyle='-', color='#4A90E2')
plt.title('Explosive Knowledge Growth After Andrew\'s Message', fontsize=16, pad=20)
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Collective Knowledge Level', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('/home/ubuntu/HARMONIA-DSL/knowledge_growth_response.png')
print('✓ Knowledge growth plot saved to knowledge_growth_response.png')

# --- Plot 2: Communication Rate Over Time ---
plt.figure(figsize=(12, 6))
# Calculate message rate per interval
message_rate = np.diff(messages) / np.diff(times)
rate_times = (np.array(times[:-1]) + np.array(times[1:])) / 2

plt.plot(rate_times, message_rate, marker='o', linestyle='-', color='#D0021B')
plt.title('Communication Rate (Messages/Sec) After Andrew\'s Message', fontsize=16, pad=20)
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Messages per Second', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('/home/ubuntu/HARMONIA-DSL/communication_rate_response.png')
print('✓ Communication rate plot saved to communication_rate_response.png')
