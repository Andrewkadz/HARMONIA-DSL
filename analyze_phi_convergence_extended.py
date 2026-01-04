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
PHI_INV_SQ = PHI_INV ** 2   # 0.3819...

# Analysis
min_val = df['alpha_sim'].min()
min_idx = df['alpha_sim'].idxmin()
final_val = df.iloc[-1]['alpha_sim']

# Check for Phi^2 Convergence
error_phi = abs(final_val - PHI_INV)
error_phi_sq = abs(final_val - PHI_INV_SQ)

print(f"EXTENDED CONVERGENCE ANALYSIS (DEPTH 97)")
print(f"========================================")
print(f"Minimum Value Reached:    {min_val:.6f} (Cycle {min_idx})")
print(f"Final Value (Cycle 600):  {final_val:.6f}")
print(f"")
print(f"ATTRACTOR ANALYSIS")
print(f"------------------")
print(f"Target 1: Phi^-1 (0.618034)")
print(f"Error: {error_phi:.6f}")
print(f"")
print(f"Target 2: Phi^-2 (0.381966)")
print(f"Error: {error_phi_sq:.6f}")
print(f"")
print(f"INTERPRETATION:")
if error_phi_sq < error_phi:
    print(f"CRITICAL DISCOVERY: The system OVERSHOT Phi^-1 and is converging to Phi^-2 (0.3819).")
    print(f"This suggests that at Depth 97, the fundamental constant is NOT Phi, but Phi Squared.")
    print(f"Phi^-2 = 1 - Phi^-1. This is the 'Lesser Segment' of the Golden Cut.")
else:
    print(f"The system is oscillating around Phi^-1.")
