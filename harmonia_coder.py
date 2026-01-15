import re
import time

class HarmoniaCoder:
    """
    The Phi Coder Engine.
    Implements the V3 Compound Symbolic Codec for high-density semantic compression.
    """
    
    # --- The V3 Codec (Compound Symbolic Logic) ---
    PHI_CODEC = {
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

        # --- COMPOUND CONCEPTS (The 11x Unlock) ---
        r"\b(entropy|chaos|disorder|noise)\b": "S↓",      # System Down
        r"\b(capacity|limit|volume|size)\b": "Λv",        # Structure Value
        r"\b(optimization|improve|better)\b": "Γ+",       # Growth Positive
        r"\b(interaction|interact)\b": "Ψx",              # Sync State
        r"\b(modulated|controlled)\b": "Φ*",              # Balance Scale
        r"\b(emergent|arising)\b": "Γ↑",                  # Growth Up
        r"\b(transformation|transform)\b": "ΔΤ",          # Change Time
        r"\b(dissipate|reduce)\b": "Ε↓",                  # Energy Down
        r"\b(maintenance|maintain)\b": "Φ=",              # Balance Equal
        r"\b(allowing|permit)\b": "Θ!",                   # Intention Do
        r"\b(creative|creation)\b": "Ξ*",                 # Seed Scale
        r"\b(structural)\b": "Λ",                         # Structure
        r"\b(dependent)\b": ":",                          # Function Of
        r"\b(function)\b": "f",                           # Function
        r"\b(vector)\b": "v",                             # Vector
        r"\b(field)\b": "F",                              # Field

        # --- ADJECTIVES & MODIFIERS (Properties) ---
        r"\b(recursive|looping|cyclic)\b": "↻",
        r"\b(rhythmic|oscillating|periodic)\b": "~",
        r"\b(internal|inner|self)\b": "•",
        r"\b(external|outer|world)\b": "°",
        r"\b(positive|good|constructive)\b": "+",
        r"\b(negative|bad|destructive)\b": "-",
        r"\b(infinite|endless|forever)\b": "∞",
        r"\b(excess|extra|surplus)\b": ">",

        # --- VERBS & ACTIONS (Vectors) ---
        r"\b(maps to|goes to|leads to|becomes|flowing into|flow into)\b": "→",
        r"\b(fused with|combined with|integrated with|harmonically fused)\b": "⊕",
        r"\b(scaled by|times)\b": "*",
        r"\b(divided by|over|ratio of)\b": "/",
        r"\b(add|plus|sum|combine)\b": "+",
        r"\b(minus|subtract|remove)\b": "-",
        r"\b(equals|is equal to|is)\b": "=",
        r"\b(not equal|unequal)\b": "≠",
        r"\b(exceeds|greater than)\b": ">",
        r"\b(less than)\b": "<",
        r"\b(must|should|have to)\b": "!",

        # --- PREPOSITIONS & LOGIC (Syntax) ---
        r"\b(of|dependent on|based on)\b": ":",
        r"\b(if|condition|when)\b": "?",
        r"\b(then|implies)\b": "!",
        r"\b(therefore|thus|so)\b": "∴",
        r"\b(while|during)\b": "@",
        r"\b(at)\b": "@",
        r"\b(and)\b": "&",
        r"\b(or)\b": "|",
        r"\b(not)\b": "¬",
        r"\b(by)\b": "*",
        r"\b(with)\b": "&"
    }

    def __init__(self):
        self.code_state = {
            "current": "",
            "history": [],
            "context": {}
        }
        # Pre-sort patterns by length (descending) to ensure greedy matching
        self.sorted_patterns = sorted(self.PHI_CODEC.keys(), key=len, reverse=True)
        
    def compress(self, text):
        """
        Compresses English text into Φπε code.
        Returns the compressed string.
        """
        try:
            compressed_text = text.lower()
            
            # 1. Apply Operator Replacements
            for pattern in self.sorted_patterns:
                symbol = self.PHI_CODEC[pattern]
                compressed_text = re.sub(pattern, symbol, compressed_text)
                
            # 2. Remove Stop Words (Aggressive)
            stop_words = [
                r"\bthe\b", r"\ba\b", r"\ban\b", r"\bis\b", r"\bare\b", 
                r"\bto\b", r"\bin\b", r"\bfor\b", 
                r"\bon\b", r"\bthis\b", r"\bthat\b", r"\bit\b", r"\bits\b"
            ]
            for sw in stop_words:
                compressed_text = re.sub(sw, "", compressed_text)
                
            # 3. Cleanup Whitespace & Punctuation
            compressed_text = re.sub(r"\s+", "", compressed_text).strip()
            compressed_text = re.sub(r"[,.]", "", compressed_text)
            
            # Update State
            self._update_state(compressed_text, text)
            
            return compressed_text
            
        except Exception as e:
            return f"Error compressing text: {str(e)}"

    def _update_state(self, code, original_text):
        """Update code state"""
        self.code_state["current"] = code
        self.code_state["history"].append({
            "code": code,
            "original": original_text,
            "timestamp": time.time()
        })
        
    def get_code_state(self):
        """Get current code state"""
        return self.code_state
        
    def clear_state(self):
        """Clear code state"""
        self.code_state = {
            "current": "",
            "history": [],
            "context": {}
        }

# --- Usage Example ---
if __name__ == "__main__":
    coder = HarmoniaCoder()
    input_text = "The goal of the system is to maintain harmonic equilibrium while allowing for infinite creative growth."
    compressed = coder.compress(input_text)
    print(f"Input: {input_text}")
    print(f"Compressed: {compressed}")
