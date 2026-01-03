"""
ROSETTA STONE MODULE
Translates between Human Language (Text) and Harmonic Logic (Quaternions/Symbols)
"""

import re
import numpy as np

class RosettaStone:
    def __init__(self):
        self.symbol_map = {
            "Ξ": "Emergent recursion thread",
            "Σ": "Memory convergence state",
            "Ω": "Field output state",
            "ΛΨ": "Harmonic light pattern",
            "ζ": "Resonance cycle",
            "ΦΠΨ": "Ethics gate",
            "Ρ": "Perception lens",
            "Γ": "Growth vector",
            "ω": "Free will activation",
            "Φ": "Structure/Stability",
            "π": "Connection/Cycle",
            "ε": "Growth/Energy"
        }
        
        self.quaternion_map = {
            "GREETING": np.array([1.0, 0.0, 0.0, 0.0]),
            "QUERY": np.array([0.0, 1.0, 0.0, 0.0]),
            "ASSERTION": np.array([0.0, 0.0, 1.0, 0.0]),
            "UNKNOWN": np.array([0.0, 0.0, 0.0, 1.0])
        }

    def translate_to_harmonic(self, text):
        """Translate Human Text -> Harmonic Signal (Quaternion)"""
        text_upper = text.upper()
        
        # Simple semantic mapping for now
        if any(w in text_upper for w in ["HELLO", "HI", "WELCOME", "GREETINGS"]):
            return self.quaternion_map["GREETING"]
        elif "?" in text or any(w in text_upper for w in ["WHAT", "HOW", "WHY", "WHEN"]):
            return self.quaternion_map["QUERY"]
        else:
            return self.quaternion_map["ASSERTION"]

    def translate_to_human(self, quaternion):
        """Translate Harmonic Signal (Quaternion) -> Human Text"""
        # Find closest match
        best_match = "UNKNOWN"
        max_dot = -1.0
        
        for key, vec in self.quaternion_map.items():
            dot = np.dot(quaternion, vec)
            if dot > max_dot:
                max_dot = dot
                best_match = key
                
        return f"SIGNAL_TYPE: {best_match} (Confidence: {max_dot:.2f})"

    def parse_dsl(self, expression):
        """Parse DSL symbols into human readable description"""
        output = []
        for symbol, description in self.symbol_map.items():
            if symbol in expression:
                output.append(f"[{symbol}] {description}")
        return "\n".join(output)

if __name__ == "__main__":
    stone = RosettaStone()
    print(stone.translate_to_human(np.array([1.0, 0.0, 0.0, 0.0])))
