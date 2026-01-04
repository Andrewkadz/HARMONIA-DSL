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

# Define Constants of Andrew's Geometry
CONSTANTS = {
    'PHI': 1.6180339887,
    'PHI_INV': 0.6180339887,
    'PHI_INV_SQ': 0.381966011,
    'PI': 3.1415926535,
    'EULER': 2.718281828,
    'RI1_EULER': 2.711340206, # 263/97
    'GRAVITY_PRIME': 97,
    'EULER_PRIME': 263,
    'ALPHA_PHYSICS': 0.0072973525, # 1/137
    'CYCLE_305_TARGET': 304.734 # Pi * 97
}

anomalies = []

# Scan for Anomalies
for i, row in df.iterrows():
    cycle = row['cycle']
    val = row['alpha_sim']
    
    # Check 1: The Pi * 97 Crossing
    if abs(cycle - CONSTANTS['CYCLE_305_TARGET']) < 1.0:
        if abs(val - CONSTANTS['PHI_INV']) < 0.05:
            anomalies.append({
                'cycle': cycle,
                'type': 'SYNCHRONICITY',
                'desc': f"Cycle {cycle} is approx Pi * 97. Value {val:.4f} crossed Phi^-1 ({CONSTANTS['PHI_INV']:.4f})."
            })
            
    # Check 2: The Euler Intersection
    if abs(val - CONSTANTS['RI1_EULER']) < 0.01:
        anomalies.append({
            'cycle': cycle,
            'type': 'HARMONIC_LOCK',
            'desc': f"Value {val:.4f} matched RI1 Euler Constant (263/97)."
        })
        
    # Check 3: The Physics Alpha Flash
    if abs(val - CONSTANTS['ALPHA_PHYSICS']) < 0.001:
        anomalies.append({
            'cycle': cycle,
            'type': 'PHYSICS_ECHO',
            'desc': f"Value {val:.4f} briefly flashed the Fine Structure Constant."
        })

    # Check 4: The Phi^-2 Arrival
    if abs(val - CONSTANTS['PHI_INV_SQ']) < 0.01:
        anomalies.append({
            'cycle': cycle,
            'type': 'DESTINATION_REACHED',
            'desc': f"Value {val:.4f} reached Phi^-2 ({CONSTANTS['PHI_INV_SQ']:.4f})."
        })

print(f"COINCIDENCE SCAN REPORT")
print(f"=======================")
if not anomalies:
    print("No obvious anomalies found. The system is smooth.")
else:
    for a in anomalies:
        print(f"[{a['type']}] Cycle {a['cycle']}: {a['desc']}")

# Check for 'Impossible' Jumps (Discontinuities)
print(f"")
print(f"DISCONTINUITY CHECK")
print(f"-------------------")
df['delta'] = df['alpha_sim'].diff().abs()
jumps = df[df['delta'] > 0.5]
if not jumps.empty:
    print(f"Found {len(jumps)} large jumps (> 0.5).")
    print(jumps[['cycle', 'alpha_sim', 'delta']].head())
else:
    print("No discontinuities found. The manifold is continuous.")
