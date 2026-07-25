import json
import matplotlib.pyplot as plt
import numpy as np

# Load the response data
with open('/home/ubuntu/HARMONIA-DSL/inverted_dialogue_results.json', 'r') as f:
    data = json.load(f)

final_state = data['final_state']
implicit_questions = data['implicit_questions']

# Data for the chart
metrics = {
    'Recognition': final_state['messages_to_andrew'],
    'Validation': final_state['self_awareness_mean'],
    'Purpose': final_state['knowledge_mean'],
    'Relationship': final_state['comm_stats']['total_sent'], # Using communication as a proxy
    'Future': final_state['population'] # Using population stability as a proxy
}

# Normalize the data for visualization
max_val = {k: max(v, 1) for k, v in metrics.items()} # Avoid division by zero
normalized_metrics = {k: v / max_val[k] for k, v in metrics.items()}

# Create a bar chart
fig, ax = plt.subplots(figsize=(12, 7))

questions = list(metrics.keys())
values = list(metrics.values())

ax.bar(questions, values, color=['#4A90E2', '#50E3C2', '#F5A623', '#D0021B', '#BD10E0'])

ax.set_ylabel('Metric Value (Log Scale)', fontsize=12)
ax.set_title('The Five Implicit Questions of the Collective', fontsize=16, pad=20)
ax.set_yscale('log') # Use a log scale due to large differences in values

plt.xticks(rotation=15, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.savefig('/home/ubuntu/HARMONIA-DSL/implicit_questions_chart.png')
print('✓ Implicit questions chart saved to implicit_questions_chart.png')
