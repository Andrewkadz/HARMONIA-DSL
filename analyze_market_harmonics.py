import pandas as pd
import numpy as np
import math

# Constants
PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI
PHI_INV_SQ = PHI_INV ** 2 # 0.381966...
PRIME_97 = 97
PRIME_263 = 263
RI1_EULER = 263 / 97 # 2.711...

def analyze_harmonics(filename, symbol):
    print(f"ANALYZING HARMONICS FOR {symbol}")
    print("==================================")
    
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df.sort_values('date')
    
    # 1. Find Major Highs and Lows
    # Simple peak detection
    window = 30
    df['min'] = df['close'].rolling(window=window, center=True).min()
    df['max'] = df['close'].rolling(window=window, center=True).max()
    
    peaks = df[df['close'] == df['max']]
    troughs = df[df['close'] == df['min']]
    
    print(f"Found {len(peaks)} major peaks and {len(troughs)} major troughs.")
    
    # 2. Check for Phi^-2 Retracements
    # A Phi^-2 retracement is when Price drops to 38.2% of the previous move.
    # Or Price drops BY 38.2% (to 61.8%).
    # Or Price drops BY 61.8% (to 38.2%).
    
    # Let's look for the "Phi^-2 Floor" (Price = Peak * 0.382)
    # This corresponds to the "Dissolution of Alpha" event in the simulation.
    
    matches = []
    
    for i in range(len(peaks) - 1):
        peak_price = peaks.iloc[i]['close']
        peak_date = peaks.iloc[i]['date']
        
        # Look forward for the next trough
        future_troughs = troughs[troughs['date'] > peak_date]
        if future_troughs.empty:
            continue
            
        next_trough = future_troughs.iloc[0]
        trough_price = next_trough['close']
        trough_date = next_trough['date']
        
        # Calculate Retracement
        drop = peak_price - trough_price
        ratio = trough_price / peak_price
        
        # Target: 0.382 (Phi^-2)
        error = abs(ratio - PHI_INV_SQ)
        
        if error < 0.05: # 5% tolerance
            matches.append({
                'type': 'PHI_INV_SQ_FLOOR',
                'peak_date': peak_date,
                'peak_price': peak_price,
                'trough_date': trough_date,
                'trough_price': trough_price,
                'ratio': ratio,
                'target': PHI_INV_SQ,
                'error': error
            })
            
    # 3. Check for Prime Time Harmonics (97 Days / 263 Days)
    # Do peaks/troughs happen 97 or 263 days apart?
    
    time_matches = []
    significant_points = pd.concat([peaks, troughs]).sort_values('date')
    
    for i in range(len(significant_points)):
        p1 = significant_points.iloc[i]
        for j in range(i + 1, len(significant_points)):
            p2 = significant_points.iloc[j]
            
            delta_days = (p2['date'] - p1['date']).days
            
            # Check 97
            if abs(delta_days - PRIME_97) <= 2:
                time_matches.append({
                    'type': 'GRAVITY_PRIME_97',
                    'date1': p1['date'],
                    'date2': p2['date'],
                    'delta': delta_days
                })
                
            # Check 263
            if abs(delta_days - PRIME_263) <= 3:
                time_matches.append({
                    'type': 'EULER_PRIME_263',
                    'date1': p1['date'],
                    'date2': p2['date'],
                    'delta': delta_days
                })

    # Report
    print(f"Phi^-2 Price Matches: {len(matches)}")
    for m in matches:
        print(f"  * {m['peak_date'].date()} (${m['peak_price']:.0f}) -> {m['trough_date'].date()} (${m['trough_price']:.0f}) | Ratio: {m['ratio']:.4f} (Target 0.382)")
        
    print(f"Prime Time Matches: {len(time_matches)}")
    # Show last 5
    for m in time_matches[-5:]:
        print(f"  * {m['type']}: {m['date1'].date()} -> {m['date2'].date()} ({m['delta']} days)")
        
    print("")

if __name__ == "__main__":
    analyze_harmonics('/home/ubuntu/HARMONIA-DSL/btc_data.csv', 'BTC')
    analyze_harmonics('/home/ubuntu/HARMONIA-DSL/spx_data.csv', 'S&P 500')
