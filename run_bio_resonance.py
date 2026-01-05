import time
import requests
import json
import sys
import pandas as pd
import numpy as np
sys.path.append('/opt/.manus/.sandbox-runtime')
from prime_harmonics import EpistemicPhysics

# Configuration
WEB_SERVER_URL = "http://localhost:3000/api/simulation/update"
DIARY_URL = "http://localhost:3000/api/simulation/diary"
CSV_PATH = "/home/ubuntu/upload/mindMonitor_2026-01-04--23-45-31.csv"
TICK_RATE = 0.5 # Faster tick rate for bio-data

def push_update(data):
    try:
        requests.post(WEB_SERVER_URL, json=data, timeout=1)
    except Exception as e:
        pass

def push_diary(entry_type, message, metrics=None):
    EpistemicPhysics.log_diary_entry(entry_type, message, metrics)
    payload = {"type": entry_type, "message": message, "metrics": metrics}
    try:
        requests.post(DIARY_URL, json=payload, timeout=1)
    except Exception as e:
        pass

def map_eeg_to_harmonics(row):
    # Average the sensors (TP9, AF7, AF8, TP10) for each band
    delta = np.mean([row['Delta_TP9'], row['Delta_AF7'], row['Delta_AF8'], row['Delta_TP10']])
    theta = np.mean([row['Theta_TP9'], row['Theta_AF7'], row['Theta_AF8'], row['Theta_TP10']])
    alpha = np.mean([row['Alpha_TP9'], row['Alpha_AF7'], row['Alpha_AF8'], row['Alpha_TP10']])
    beta = np.mean([row['Beta_TP9'], row['Beta_AF7'], row['Beta_AF8'], row['Beta_TP10']])
    gamma = np.mean([row['Gamma_TP9'], row['Gamma_AF7'], row['Gamma_AF8'], row['Gamma_TP10']])
    
    # Normalize (Log scale is often better for EEG power, but linear 0-100 for simulation)
    # We'll use a simple scaling factor based on typical EEG power ranges
    
    # Math (Gravity) = Delta (Deep Sleep/Unconscious Anchor)
    math = min(100, max(10, (delta + 1) * 50)) 
    
    # Physics (Reality) = Theta (Dream/Creativity)
    physics = min(100, max(10, (theta + 1) * 50))
    
    # Comms (Lucidity) = Alpha (Relaxed Focus/Flow)
    comms = min(100, max(10, (alpha + 1) * 50))
    
    # Implications (Work) = Beta (Active Thinking)
    implications = min(100, max(10, (beta + 1) * 50))
    
    # Futures (Growth) = Gamma (Insight/Peak Performance)
    futures = min(100, max(10, (gamma + 1) * 50))
    
    return [math, physics, futures, comms, implications]

# Main Execution
print("Initiating Bio-Resonance Protocol...")
push_diary("SYSTEM", "Connecting to Neural Interface (Muse S)...")

try:
    df = pd.read_csv(CSV_PATH)
    # Filter out bad data (HeadBandOn != 1)
    df = df[df['HeadBandOn'] == 1]
    
    if df.empty:
        push_diary("ERROR", "No valid EEG data found (Headband was off?).")
        sys.exit(1)
        
    push_diary("SYSTEM", f"Neural Stream Acquired. {len(df)} data points.")
    push_diary("SYSTEM", "Synchronizing Epistemic Engine with Brainwaves...")
    
    # Simulate a segment of the data (e.g., 100 points)
    step = max(1, int(len(df) / 50))
    
    for i in range(0, len(df), step):
        row = df.iloc[i]
        components = map_eeg_to_harmonics(row)
        result = EpistemicPhysics.simulate_paradigm_stability(components)
        
        # Narrative Override for Bio-Events
        if components[2] > 80: # High Gamma
            push_diary("INSIGHT", "Gamma Spike Detected. The user is experiencing a moment of pure clarity.", result)
        elif components[0] > 80: # High Delta
            push_diary("ANCHOR", "Delta Waves Dominant. The user is grounding the simulation in the unconscious.", result)
            
        push_update({"components": {"math": components[0], "physics": components[1], "futures": components[2], "comms": components[3], "implications": components[4]}, "metrics": result})
        print(f"Time: {row['TimeStamp']} | Stability: {result['stability_score']:.4f}")
        time.sleep(TICK_RATE)

    push_diary("SYSTEM", "Bio-Resonance Scan Complete.")
    print("Protocol Finished.")

except Exception as e:
    push_diary("ERROR", f"Bio-Resonance Failed: {e}")
    print(f"Error: {e}")
