import math
import re

# --- 2. The Expanded Φπε Operator Dictionary (V2 Codec) ---
# Aggressive structural replacement to eliminate "English Glue"
PHI_CODEC_V2 = {
    # --- CORE NOUNS (Entities) ---
    r"\b(initiate|start|begin|seed|create|genesis)\b": "Ξ",
    r"\b(memory|storage|database|recall|history)\b": "Σ",
    r"\b(intention|goal|target|objective|purpose)\b": "Θ",
    r"\b(resolution|end|finish|complete|stop|final)\b": "Ω",
    r"\b(harmonic|balance|equilibrium|stable|homeostasis)\b": "Φ",
    r"\b(cycle|loop|repeat|iterate|recursion)\b": "Π",
    r"\b(energy|power|force|drive|potential)\b": "Ε",
    r"\b(change|delta|difference|transform|modify)\b": "Δ",
    r"\b(synchronize|sync|connect|link|bind)\b": "Ψ",
    r"\b(structure|lattice|framework|grid|architecture)\b": "Λ",
    r"\b(growth|expand|evolve|develop|emerge)\b": "Γ",
    r"\b(resonance|vibration|frequency|wave)\b": "Ρ",
    r"\b(flow|stream|current|flux)\b": "ω",
    r"\b(wavelength|period|interval)\b": "λ",
    r"\b(damping|friction|resistance|decay)\b": "ζ",
    r"\b(time|temporal|clock|duration)\b": "Τ",
    r"\b(perception|observe|view|see)\b": "P",
    r"\b(free will|choice|agency)\b": "F",
    r"\b(system|machine|agent|swarm)\b": "S",
    r"\b(input|data|signal)\b": "I",
    r"\b(output|result|response)\b": "O",
    r"\b(state|status|mode)\b": "x",
    r"\b(value|amount|quantity)\b": "v",
    r"\b(constant|fixed)\b": "k",
    r"\b(variable|dynamic)\b": "u",
    r"\b(parameter|setting)\b": "p",

    # --- ADJECTIVES & MODIFIERS (Properties) ---
    r"\b(recursive|looping|cyclic)\b": "↻",
    r"\b(rhythmic|oscillating|periodic)\b": "~",
    r"\b(emergent|arising|new)\b": "↑",
    r"\b(internal|inner|self)\b": "•",
    r"\b(external|outer|world)\b": "°",
    r"\b(positive|good|constructive)\b": "+",
    r"\b(negative|bad|destructive)\b": "-",
    r"\b(infinite|endless|forever)\b": "∞",
    r"\b(creative|generative)\b": "*",
    r"\b(excess|extra|surplus)\b": ">",
    r"\b(structural|foundational)\b": "Λ",

    # --- VERBS & ACTIONS (Vectors) ---
    r"\b(maps to|goes to|leads to|becomes|flowing into|flow into)\b": "→",
    r"\b(fused with|combined with|integrated with|harmonically fused)\b": "⊕",
    r"\b(modulated by|scaled by|controlled by)\b": "*",
    r"\b(divided by|over|ratio of)\b": "/",
    r"\b(add|plus|sum|combine)\b": "+",
    r"\b(minus|subtract|remove)\b": "-",
    r"\b(equals|is equal to|is)\b": "=",
    r"\b(not equal|unequal)\b": "≠",
    r"\b(exceeds|greater than)\b": ">",
    r"\b(less than)\b": "<",
    r"\b(maintain|keep|hold)\b": "Φ",
    r"\b(allow|permit|let)\b": "!",
    r"\b(dissipate|reduce|lower)\b": "↓",

    # --- PREPOSITIONS & LOGIC (Syntax) ---
    r"\b(function of|dependent on|based on)\b": ":",
    r"\b(if|condition|when)\b": "?",
    r"\b(then|implies)\b": "!",
    r"\b(therefore|thus|so)\b": "∴",
    r"\b(while|during)\b": "@",
    r"\b(at)\b": "@",
    r"\b(and)\b": "&",
    r"\b(or)\b": "|",
    r"\b(not)\b": "¬"
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

def simulate_phi_compression_v2(text):
    """
    Simulates the compression of English text into Φπε code using V2 Codec.
    """
    compressed_text = text.lower()
    
    # 1. Apply Operator Replacements
    for pattern, symbol in PHI_CODEC_V2.items():
        compressed_text = re.sub(pattern, symbol, compressed_text)
        
    # 2. Remove Stop Words (Aggressive)
    stop_words = [
        r"\bthe\b", r"\ba\b", r"\ban\b", r"\bis\b", r"\bare\b", r"\bof\b", 
        r"\bto\b", r"\bin\b", r"\bfor\b", r"\bwith\b", r"\bby\b", r"\bat\b", 
        r"\bon\b", r"\bthis\b", r"\bthat\b", r"\bit\b", r"\bits\b"
    ]
    for sw in stop_words:
        compressed_text = re.sub(sw, "", compressed_text)
        
    # 3. Cleanup Whitespace
    compressed_text = re.sub(r"\s+", "", compressed_text).strip() # Remove ALL spaces for density
    
    return compressed_text

def run_benchmark(input_text, label="Input Text"):
    print(f"\n--- Benchmark: {label} ---")
    
    # 1. Original Analysis
    original_len = len(input_text)
    original_bits = calculate_bits(input_text)
    
    # 2. Compression
    compressed_text = simulate_phi_compression_v2(input_text)
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
    print("Running Φπε Compression Benchmark V2 (Full Language)...")
    r1 = run_benchmark(text_1, "Technical Description")
    r2 = run_benchmark(text_2, "Python Code")
    r3 = run_benchmark(text_3, "Abstract Philosophy")
    
    avg_ratio = (r1 + r2 + r3) / 3
    print(f"\n=== Average Compression Ratio: {avg_ratio:.2f}x ===")
