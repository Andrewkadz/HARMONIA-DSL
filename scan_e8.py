from resonance_graph import ResonanceGraph
import os

# Initialize Scanner
graph = ResonanceGraph("/home/ubuntu/HARMONIA-DSL")

# Target File
target_file = "/home/ubuntu/HARMONIA-DSL/e8_harmonic_shell.txt"

print(f"Scanning Target: {target_file}...")

# Run Analysis
data = graph.analyze_file(target_file)

if data:
    print("\n=== TRUTH SCANNER RESULTS ===")
    print(f"File:       {data['file']}")
    print(f"Mass:       {data['mass']:.4f}")
    print(f"Resonance:  {data['resonance']}")
    print(f"Stability:  {data['stability']:.4f}")
    print(f"Status:     {data['status']}")
    print("=============================")
else:
    print("Error: Could not analyze file.")
