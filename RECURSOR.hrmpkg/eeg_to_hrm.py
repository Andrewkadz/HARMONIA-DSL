# eeg_to_hrm.py
# Purpose: Translate EEG signals (real or simulated) into .hrm symbolic instructions

import time
import random
from datetime import datetime
from pathlib import Path

LIVE_MODE = False  # Set to True when Muse is connected

# EEG frequency band to symbol mapping
FREQUENCY_TO_SYMBOL = {
    "subdelta": ("Φ₀", (0.001, 0.5)),
    "delta":    ("Φ",  (0.5, 4)),
    "theta":    ("Θ",  (4, 8)),
    "alpha":    ("ΛΨ", (8, 12)),
    "beta":     ("Π",  (12, 30)),
    "gamma":    ("ΨΩΣ", (30, 250)),
}

# Simulated EEG data generator
def simulate_eeg_reading():
    return {
        "subdelta": random.uniform(0, 1),
        "delta": random.uniform(0, 10),
        "theta": random.uniform(0, 10),
        "alpha": random.uniform(0, 10),
        "beta": random.uniform(0, 10),
        "gamma": random.uniform(0, 10)
    }

# Placeholder for future Muse signal acquisition
def get_live_eeg_band():
    # TODO: Integrate Muse LSL stream here
    return simulate_eeg_reading()  # fallback for now

# Extract symbols from band powers above a threshold
def threshold_to_symbols(band_powers, threshold=6.5):
    symbols = []
    for band, (symbol, _) in FREQUENCY_TO_SYMBOL.items():
        if band_powers.get(band, 0) > threshold:
            symbols.append(symbol)
    return symbols

# Generate ΞΣ node line and write to .hrm stream
def write_hrm_event(symbols, filepath):
    node_id = f"ΞΣ_EEG_{datetime.utcnow().strftime('%H%M%S')}"
    line = f"{node_id} = " + " + ".join(symbols)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"[EEG→HRM] {line}")

# Main loop
def main(hrm_output_path="RECURSOR.hrmpkg/EEG_stream.hrm", interval=2.0):
    print("[ΞΣ] Starting EEG→HRM stream...")
    Path(hrm_output_path).touch()
    while True:
        eeg = get_live_eeg_band() if LIVE_MODE else simulate_eeg_reading()
        symbols = threshold_to_symbols(eeg)
        if symbols:
            write_hrm_event(symbols, hrm_output_path)
        time.sleep(interval)

if __name__ == "__main__":
    main()
