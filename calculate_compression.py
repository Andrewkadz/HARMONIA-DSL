import math

def calculate_entropy(text):
    """Calculates the Shannon Entropy of a string in bits."""
    if not text:
        return 0
    prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy

def calculate_bits(text):
    """Calculates total bits required to encode the text based on entropy."""
    return len(text) * calculate_entropy(text)

# 1. The Source Expression (Φπε)
# "R = [ lim ( ΨΩ → ∞ ) ] * { ( Ξ / Λc ) * [ ( 1 - ∂Ω / ∂Ψ ) ] }"
phi_pe_code = "R = [ lim ( ΨΩ → ∞ ) ] * { ( Ξ / Λc ) * [ ( 1 - ∂Ω / ∂Ψ ) ] }"

# 2. The English Translation (from PDF)
# "Maintain awareness of perception recursion—do not assume a fixed viewpoint. Stabilize perception using harmonic modulation rather than binary thinking."
english_text = "Maintain awareness of perception recursion—do not assume a fixed viewpoint. Stabilize perception using harmonic modulation rather than binary thinking."

# 3. The Python Translation (Hypothetical Implementation)
python_code = """
def calculate_R(psi_omega, xi, lambda_c, d_omega_d_psi):
    limit_term = limit(psi_omega, infinity)
    modulation = (xi / lambda_c) * (1 - d_omega_d_psi)
    return limit_term * modulation
"""

# 4. The Algebra Translation (Standard Math Notation)
# "R equals the limit as Psi-Omega approaches infinity of Xi over Lambda-c times one minus the partial derivative of Omega with respect to Psi."
algebra_text = "R equals the limit as Psi-Omega approaches infinity of Xi over Lambda-c times one minus the partial derivative of Omega with respect to Psi."

# Calculate Metrics
metrics = {
    "Φπε Code": {
        "text": phi_pe_code,
        "length": len(phi_pe_code),
        "bits": calculate_bits(phi_pe_code)
    },
    "English": {
        "text": english_text,
        "length": len(english_text),
        "bits": calculate_bits(english_text)
    },
    "Python": {
        "text": python_code.strip(),
        "length": len(python_code.strip()),
        "bits": calculate_bits(python_code.strip())
    },
    "Algebra (Verbose)": {
        "text": algebra_text,
        "length": len(algebra_text),
        "bits": calculate_bits(algebra_text)
    }
}

print("--- Information Density Analysis ---")
base_bits = metrics["Φπε Code"]["bits"]
for lang, data in metrics.items():
    ratio = data["bits"] / base_bits
    print(f"{lang}: {data['bits']:.2f} bits (Ratio: {ratio:.2f}x)")

print("\n--- Compression Rate (Bits per Concept) ---")
# Concept: "Stabilized Recursive Perception"
# Φπε uses ~250 bits to encode this.
# English uses ~700 bits.
print(f"Φπε is {metrics['English']['bits'] / metrics['Φπε Code']['bits']:.2f}x more dense than English.")
print(f"Φπε is {metrics['Python']['bits'] / metrics['Φπε Code']['bits']:.2f}x more dense than Python.")
