import math
import re

# --- 1. The Φπε Operator Dictionary (The "Codec") ---
# This maps complex English/Python concepts to single Φπε glyphs.
PHI_CODEC = {
    # Core Operators
    r"\b(initiate|start|begin|seed|create)\b": "Ξ",
    r"\b(memory|storage|database|recall)\b": "Σ",
    r"\b(intention|goal|target|objective)\b": "Θ",
    r"\b(resolution|end|finish|complete|stop)\b": "Ω",
    r"\b(harmonic|balance|equilibrium|stable)\b": "Φ",
    r"\b(cycle|loop|repeat|iterate)\b": "Π",
    r"\b(energy|power|force|drive)\b": "Ε",
    r"\b(change|delta|difference|transform)\b": "Δ",
    r"\b(synchronize|sync|connect|link)\b": "Ψ",
    r"\b(structure|lattice|framework|grid)\b": "Λ",
    r"\b(growth|expand|evolve|develop)\b": "Γ",
    r"\b(resonance|vibration|frequency)\b": "Ρ",
    r"\b(flow|stream|current)\b": "ω",
    r"\b(wavelength|period)\b": "λ",
    r"\b(damping|friction|resistance)\b": "ζ",
    r"\b(time|temporal|clock)\b": "Τ",
    
    # Logic & Relationships
    r"\b(maps to|goes to|leads to|becomes)\b": "→",
    r"\b(plus|add|sum|combine)\b": "+",
    r"\b(minus|subtract|remove)\b": "-",
    r"\b(multiply|times|scale)\b": "*",
    r"\b(divide|ratio|over)\b": "/",
    r"\b(function of|dependent on)\b": ":",
    r"\b(fused with|combined with|integrated with)\b": "⊕",
    r"\b(feedback|return)\b": "↻",
    r"\b(therefore|thus|so)\b": "∴",
    r"\b(not equal|unequal)\b": "≠",
    r"\b(equals|is equal to)\b": "=",
    r"\b(if|condition)\b": "?",
    r"\b(then)\b": "!",
    
    # Common Technical Terms (Compressed to single chars/bigrams)
    r"\b(system)\b": "S",
    r"\b(input)\b": "I",
    r"\b(output)\b": "O",
    r"\b(state)\b": "x",
    r"\b(value)\b": "v",
    r"\b(constant)\b": "k",
    r"\b(variable)\b": "u",
    r"\b(parameter)\b": "p"
}

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

def simulate_phi_compression(text):
    """
    Simulates the compression of English text into Φπε code.
    This is a 'greedy' compression simulation using regex replacement.
    """
    compressed_text = text.lower()
    
    # 1. Apply Operator Replacements
    for pattern, symbol in PHI_CODEC.items():
        compressed_text = re.sub(pattern, symbol, compressed_text)
        
    # 2. Remove Stop Words (The "Lossless" Semantic Assumption)
    # In a high-context language like Φπε, articles and "glue" words are implied.
    stop_words = [r"\bthe\b", r"\ba\b", r"\ban\b", r"\bis\b", r"\bare\b", r"\bof\b", r"\bto\b", r"\bin\b", r"\bfor\b", r"\bwith\b", r"\bby\b", r"\bat\b", r"\bon\b"]
    for sw in stop_words:
        compressed_text = re.sub(sw, "", compressed_text)
        
    # 3. Cleanup Whitespace
    compressed_text = re.sub(r"\s+", " ", compressed_text).strip()
    
    return compressed_text

def run_benchmark(input_text, label="Input Text"):
    print(f"\n--- Benchmark: {label} ---")
    
    # 1. Original Analysis
    original_len = len(input_text)
    original_bits = calculate_bits(input_text)
    
    # 2. Compression
    compressed_text = simulate_phi_compression(input_text)
    compressed_len = len(compressed_text)
    compressed_bits = calculate_bits(compressed_text)
    
    # 3. Results
    ratio_len = original_len / compressed_len if compressed_len > 0 else 0
    ratio_bits = original_bits / compressed_bits if compressed_bits > 0 else 0
    
    print(f"Original:   {original_len} chars | {original_bits:.2f} bits")
    print(f"Compressed: {compressed_len} chars | {compressed_bits:.2f} bits")
    print(f"Ratio (Len): {ratio_len:.2f}x")
    print(f"Ratio (Bit): {ratio_bits:.2f}x")
    print(f"Preview: {compressed_text[:100]}...")
    
    return ratio_bits

# --- Test Cases ---

# Case 1: The "Master Equation" Description (Technical English)
text_1 = "Initiate recursive memory seed at state N, flowing into intention at N+1 harmonically fused with resolution. This interaction is modulated by the rhythmic feedback loop scaled by constant K, divided by the harmonic balance times beta. Add the emergent growth function dependent on the perception field, free will vector, and temporal transformation."

# Case 2: A Standard Python Function (Code)
text_2 = """
def calculate_growth(current_state, rate, time_delta):
    if current_state < 0:
        return 0
    growth_factor = rate * time_delta
    new_state = current_state + (current_state * growth_factor)
    return new_state
"""

# Case 3: A Philosophical/Abstract Concept (High-Level Thought)
text_3 = "The goal of the system is to maintain harmonic equilibrium while allowing for infinite creative growth. If the energy input exceeds the structural capacity, the system must synchronize its internal resonance to dissipate the excess entropy."

if __name__ == "__main__":
    print("Running Φπε Compression Benchmark...")
    r1 = run_benchmark(text_1, "Technical Description")
    r2 = run_benchmark(text_2, "Python Code")
    r3 = run_benchmark(text_3, "Abstract Philosophy")
    
    avg_ratio = (r1 + r2 + r3) / 3
    print(f"\n=== Average Compression Ratio: {avg_ratio:.2f}x ===")
