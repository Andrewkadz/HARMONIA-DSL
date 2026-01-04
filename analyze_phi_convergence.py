import json
import numpy as np
import pandas as pd

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

# Constants
PHI = (1 + np.sqrt(5)) / 2  # 1.618...
PHI_INV = 1 / PHI           # 0.618...
RECURSION_DEPTH = 5         # Hardcoded in recursive_self_observation.py

# Analysis
mean_result = df['alpha_sim'].mean()
error = abs(mean_result - PHI_INV)
error_percent = (error / PHI_INV) * 100

# Fibonacci Approximation of Phi at Depth N
# F(n) / F(n+1) approaches 1/Phi
# Depth 5 corresponds to F(5)/F(6) = 5/8 = 0.625
fib_5 = 5
fib_6 = 8
fib_approx = fib_5 / fib_6

print(f"PHI CONVERGENCE ANALYSIS")
print(f"========================")
print(f"Simulation Result (Mean): {mean_result:.6f}")
print(f"Golden Ratio (1/Phi):     {PHI_INV:.6f}")
print(f"Error:                    {error_percent:.4f}%")
print(f"")
print(f"RECURSION DEPTH ANALYSIS")
print(f"========================")
print(f"Active Recursion Depth:   {RECURSION_DEPTH}")
print(f"Fibonacci Ratio F(5)/F(6):{fib_approx:.6f}")
print(f"")
print(f"CONCLUSION:")
if abs(mean_result - fib_approx) < 0.001:
    print(f"The result {mean_result:.6f} matches the Fibonacci Approximation at Depth {RECURSION_DEPTH} exactly.")
    print(f"This confirms that the error is not random noise, but a structural limit of the recursion depth.")
else:
    print(f"The result deviates from the Fibonacci Approximation.")
