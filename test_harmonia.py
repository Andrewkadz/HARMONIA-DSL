from systemic_integration import HarmoniaSystemIntegrator

# Create system
harmonia = HarmoniaSystemIntegrator()

# Test input
state = {
    'psi': 12.0,
    'phi': 9.0,
    'velocity': 1.5,
    'knowledge': 0.8,
    'energy': 90.0,
    'epsilon': 0.15,
}

# Process
result = harmonia.process(state)

print("\u2713 HARMONIA Core Working")
print(f"  R (Response): {result['R']:.3f}")
print(f"  \u03a3 (Stability): {result.get('sigma', 'N/A')}")
