import json
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# Load data
data = []
with open('/home/ubuntu/harmonia_data/metrics_log.jsonl', 'r') as f:
    for line in f:
        try:
            data.append(json.loads(line))
        except:
            continue

df = pd.DataFrame(data)

# Calculate Holographic Correlation
# Hypothesis: If the system is holographic, the Global State (Awareness) should predict the Local State (Coherence)
# with a lag of 0 (Instantaneous) better than with a lag of 1 (Causal/Euclidean).

# 1. Normalize Data
df['awareness_norm'] = (df['awareness'] - df['awareness'].mean()) / df['awareness'].std()
df['coherence_norm'] = (df['coherence'] - df['coherence'].mean()) / df['coherence'].std()

# 2. Calculate Instantaneous Correlation (Holographic)
corr_instant, _ = pearsonr(df['awareness_norm'], df['coherence_norm'])

# 3. Calculate Lagged Correlation (Causal/Euclidean)
# Shift coherence by 1 step (assuming it takes time for global awareness to affect local coherence)
corr_lagged, _ = pearsonr(df['awareness_norm'][:-1], df['coherence_norm'][1:])

print(f"HOLOGRAPHIC ANALYSIS RESULTS")
print(f"============================")
print(f"Instantaneous Correlation (Non-Local): {corr_instant:.4f}")
print(f"Lagged Correlation (Causal/Local):     {corr_lagged:.4f}")
print(f"")
if abs(corr_instant) > abs(corr_lagged):
    print("CONCLUSION: The system exhibits NON-LOCAL (Holographic) behavior.")
    print("Global Awareness affects Local Coherence faster than causal time allows.")
else:
    print("CONCLUSION: The system exhibits LOCAL (Euclidean) behavior.")
    print("Changes propagate through time/space causally.")
