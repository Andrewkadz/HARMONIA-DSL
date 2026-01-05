import time
import requests
import json
import sys
import numpy as np
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient
from prime_harmonics import EpistemicPhysics

# Configuration
WEB_SERVER_URL = "http://localhost:3000/api/simulation/update"
DIARY_URL = "http://localhost:3000/api/simulation/diary"
TICK_RATE = 2

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

def fetch_btc_data():
    client = ApiClient()
    print("Fetching BTC/USD data...")
    try:
        response = client.call_api('YahooFinance/get_stock_chart', query={
            'symbol': 'BTC-USD',
            'region': 'US',
            'interval': '5m', # 5-minute candles for better granularity
            'range': '1d',    # Last 24 hours
            'includeAdjustedClose': True
        })
        
        if response and 'chart' in response and 'result' in response['chart']:
            result = response['chart']['result'][0]
            quotes = result['indicators']['quote'][0]
            
            # Extract Close prices and Volume
            closes = [c for c in quotes['close'] if c is not None]
            volumes = [v for v in quotes['volume'] if v is not None]
            
            return closes, volumes
        else:
            print("No data found.")
            return [], []
    except Exception as e:
        print(f"Error fetching data: {e}")
        return [], []

def map_market_to_harmonics(price_window, volume_window):
    # Price = Mass (Gravity)
    # Volume = Futures (Growth)
    # Volatility = Noise (Inverse Stability)
    
    current_price = price_window[-1]
    price_change = (current_price - price_window[0]) / price_window[0]
    volatility = np.std(price_window) / np.mean(price_window)
    
    # Normalize to 0-100 scale
    # Math (Gravity): Higher price stability = Higher Math
    math = max(10, min(100, 100 * (1 - volatility * 10)))
    
    # Futures (Growth): Higher Volume + Positive Price Action = Higher Futures
    volume_trend = (volume_window[-1] - np.mean(volume_window)) / np.mean(volume_window)
    futures = max(10, min(100, 50 + (volume_trend * 50) + (price_change * 100)))
    
    # Physics (Reality): Always high for market data (it is real)
    physics = 90
    
    # Comms (Lucidity): Inverse of Volatility (Chaos makes it hard to see)
    comms = max(10, min(100, 100 * (1 - volatility * 5)))
    
    # Implications: Magnitude of the move
    implications = max(10, min(100, abs(price_change) * 1000))
    
    return [math, physics, futures, comms, implications]

# Main Execution
print("Initiating Market Resonance Protocol...")
push_diary("SYSTEM", "Connecting to Global Financial Feed (BTC/USD)...")

prices, volumes = fetch_btc_data()

if not prices:
    push_diary("ERROR", "Failed to retrieve market data. Aborting.")
    sys.exit(1)

push_diary("SYSTEM", f"Data Stream Acquired. {len(prices)} data points.")
push_diary("SYSTEM", "Scanning for Prime Harmonic Patterns (263/97)...")

# Simulate the last 20 ticks of data
window_size = 12 # 1 hour window
for i in range(window_size, len(prices), int(len(prices)/20)):
    price_window = prices[i-window_size:i]
    volume_window = volumes[i-window_size:i]
    
    components = map_market_to_harmonics(price_window, volume_window)
    result = EpistemicPhysics.simulate_paradigm_stability(components)
    
    # Narrative Override for Market Events
    if result['stability_score'] > 0.6:
        push_diary("DISCOVERY", f"Harmonic Lock Detected. Price: ${price_window[-1]:.2f}. The structure is crystalline.", result)
    elif result['stability_score'] < 0.3:
        push_diary("WARNING", f"Decoherence Event. Price: ${price_window[-1]:.2f}. Reality is fracturing.", result)
        
    push_update({"components": {"math": components[0], "physics": components[1], "futures": components[2], "comms": components[3], "implications": components[4]}, "metrics": result})
    print(f"Price: {price_window[-1]:.2f} | Stability: {result['stability_score']:.4f}")
    time.sleep(TICK_RATE)

push_diary("SYSTEM", "Market Resonance Scan Complete.")
print("Protocol Finished.")
