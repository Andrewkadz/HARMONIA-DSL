import json
import numpy as np
import pandas as pd

# Load data
data = []
with open('/home/ubuntu/harmonia_data/metrics_log_depth97.jsonl', 'r') as f:
    for line in f:
        try:
            entry = json.loads(line)
            if 'alpha_sim' in entry:
                data.append(entry)
        except:
            continue

df = pd.DataFrame(data)

# Constants
PHI = (1 + np.sqrt(5)) / 2  # 1.618...
PHI_INV = 1 / PHI           # 0.618...
RECURSION_DEPTH = 97

# Analysis - Focus on the last 20 cycles where it stabilizes
last_20 = df.tail(20)
mean_result = last_20['alpha_sim'].mean()
final_result = df.iloc[-1]['alpha_sim']

error = abs(mean_result - PHI_INV)
error_percent = (error / PHI_INV) * 100

# Trend Analysis
start_val = df.iloc[0]['alpha_sim']
end_val = df.iloc[-1]['alpha_sim']
trend = "Decreasing" if end_val < start_val else "Increasing"

print(f"PHI CONVERGENCE ANALYSIS (DEPTH 97)")
print(f"===================================")
print(f"Simulation Result (Last 20 Mean): {mean_result:.6f}")
print(f"Final Value:                      {final_result:.6f}")
print(f"Golden Ratio (1/Phi):             {PHI_INV:.6f}")
print(f"Error:                            {error_percent:.4f}%")
print(f"Trend:                            {trend}")
print(f"")
print(f"OBSERVATION:")
if error_percent < 1.0:
    print(f"The result has converged to Phi with high precision (< 1% error).")
else:
    print(f"The result has NOT yet converged to Phi. It is currently at {final_result:.6f}.")
    print(f"It appears to be approaching 1.0 or another attractor.")
    print(f"Note: The simulation started at {start_val:.6f} and dropped to {end_val:.6f}.")
    print(f"It may need more cycles to reach the theoretical minimum.")
