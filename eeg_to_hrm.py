import os

# Create the EEG to HRM converter Python script content
eeg_to_hrm_code = '''
import csv

# EEG band definitions (Hz ranges) with symbolic mappings
EEG_BANDS = {
    "ε": (0.001, 0.01),       # Ultra-low
    "Φ₀": (0.01, 0.5),        # Subdelta
    "Φ": (0.5, 4),            # Delta
    "Θ": (4, 8),              # Theta
    "ΛΨ": (8, 12),            # Alpha
    "ΞΣ": (12, 30),           # Beta
    "ωΩ": (30, 100),          # Gamma
    "ΨΩΣ": (100, 250)         # High Gamma
}

def map_frequency_to_symbol(freq):
    for symbol, (low, high) in EEG_BANDS.items():
        if low <= freq < high:
            return symbol
    return None

def generate_hrm_from_eeg(input_csv_path, output_hrm_path, threshold=0.4):
    active_symbols = set()

    with open(input_csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for band, power_str in row.items():
                try:
                    freq = float(band)
                    power = float(power_str)
                    if power > threshold:
                        symbol = map_frequency_to_symbol(freq)
                        if symbol:
                            active_symbols.add(symbol)
                except ValueError:
                    continue

    with open(output_hrm_path, 'w') as f:
        f.write('// GENERATED FROM EEG INPUT\\n')
        if active_symbols:
            hrm_expr = 'ΞΣ₀ = ' + ' + '.join(active_symbols)
            f.write(hrm_expr + '\\n')
            if "ΨΩΣ" in active_symbols:
                f.write('trigger: ΞΣ(n+1)\\n')
        else:
            f.write('// No significant neural activity detected above threshold\\n')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert EEG CSV to symbolic HRM file.")
    parser.add_argument("--input", required=True, help="Path to EEG CSV input file.")
    parser.add_argument("--output", required=True, help="Path to output HRM file.")
    parser.add_argument("--threshold", type=float, default=0.4, help="Threshold for signal strength (default 0.4).")
    args = parser.parse_args()
    generate_hrm_from_eeg(args.input, args.output, args.threshold)
'''

# Save the script to file
output_path = "/mnt/data/eeg_to_hrm.py"
with open(output_path, "w") as file:
    file.write(eeg_to_hrm_code)

output_path
