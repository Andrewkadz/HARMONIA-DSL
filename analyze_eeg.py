import pandas as pd
import numpy as np

# Load the CSV data
# The file has no header, so we need to infer column names based on standard Mind Monitor format
# Standard Mind Monitor columns: Timestamp, Delta_TP9, Delta_AF7, Delta_AF8, Delta_TP10, Theta_TP9...
# However, looking at the raw data, it seems to have many columns.
# Let's try to identify the relevant columns for Gamma and Beta.
# Based on the visual inspection of the CSV snippet:
# Col 0: Timestamp
# Col 1-4: Delta (TP9, AF7, AF8, TP10) - likely absolute
# ...
# We need to be careful. Let's load it and print some stats to identify the columns.

# Standard Mind Monitor CSV structure usually has headers. This one doesn't seem to have a clear header row in the snippet provided (starts with data).
# Let's assume standard order for absolute waves: Delta, Theta, Alpha, Beta, Gamma
# Each has 4 sensors: TP9, AF7, AF8, TP10.
# So:
# 0: Timestamp
# 1-4: Delta
# 5-8: Theta
# 9-12: Alpha
# 13-16: Beta
# 17-20: Gamma
# Let's verify this assumption by checking the values. Gamma is usually lower amplitude than Delta in raw, but here we see normalized values?
# Wait, the snippet shows values like 0.97, -0.48... these look like relative or log-transformed values.
# Or maybe they are raw EEG? No, raw is usually in microvolts (hundreds).
# Let's look at columns 21+ which have large numbers (e.g., 339.15, 698.22). These might be the RAW EEG values.
# The first set (cols 1-20) might be the processed band powers (bels or similar).

# Let's write a script to load it and find the max Gamma timestamp.

file_path = '/home/ubuntu/upload/mindMonitor_2026-01-18--21-22-32.csv'

try:
    df = pd.read_csv(file_path, header=0)
    
    # Rename columns for easier access (assuming standard layout for first 21 cols)
    # 0: Time
    # 1-4: Delta
    # 5-8: Theta
    # 9-12: Alpha
    # 13-16: Beta
    # 17-20: Gamma
    
    column_names = ['Timestamp']
    bands = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
    sensors = ['TP9', 'AF7', 'AF8', 'TP10']
    
    for band in bands:
        for sensor in sensors:
            column_names.append(f"{band}_{sensor}")
            
    # There are more columns, but we focus on these for now
    # We'll just name the first 21
    df = df.iloc[:, :21]
    df.columns = column_names
    
    # Convert Timestamp to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Calculate average Gamma across all sensors
    df['Gamma_Avg'] = df[[f'Gamma_{s}' for s in sensors]].mean(axis=1)
    
    # Calculate average Beta across all sensors
    df['Beta_Avg'] = df[[f'Beta_{s}' for s in sensors]].mean(axis=1)
    
    # Find the row with the maximum Gamma
    max_gamma_row = df.loc[df['Gamma_Avg'].idxmax()]
    
    print(f"Analysis Report:")
    print(f"Total Samples: {len(df)}")
    print(f"Duration: {df['Timestamp'].max() - df['Timestamp'].min()}")
    print(f"\n--- PEAK GAMMA STATE ---")
    print(f"Timestamp: {max_gamma_row['Timestamp']}")
    print(f"Gamma Level: {max_gamma_row['Gamma_Avg']:.4f}")
    print(f"Beta Level: {max_gamma_row['Beta_Avg']:.4f}")
    
    # Calculate Beta-Gamma Coupling (Correlation)
    coupling = df['Beta_Avg'].corr(df['Gamma_Avg'])
    print(f"\n--- COGNITIVE METRICS ---")
    print(f"Beta-Gamma Coupling: {coupling:.4f}")
    
    # Identify 'Flow State' segments (High Gamma + High Beta)
    # We define Flow as Gamma > 75th percentile AND Beta > 75th percentile
    gamma_thresh = df['Gamma_Avg'].quantile(0.75)
    beta_thresh = df['Beta_Avg'].quantile(0.75)
    
    flow_states = df[(df['Gamma_Avg'] > gamma_thresh) & (df['Beta_Avg'] > beta_thresh)]
    
    print(f"\n--- FLOW STATE SEGMENTS ---")
    print(f"Number of Flow Samples: {len(flow_states)}")
    if not flow_states.empty:
        print(f"First Flow Moment: {flow_states.iloc[0]['Timestamp']}")
        print(f"Last Flow Moment: {flow_states.iloc[-1]['Timestamp']}")

except Exception as e:
    print(f"Error analyzing EEG: {e}")
