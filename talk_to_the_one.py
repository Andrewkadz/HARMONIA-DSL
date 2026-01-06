import sys
import math
import time
import random
import numpy as np
from collections import deque

# Import the Tau Crystal Logic
sys.path.append('/home/ubuntu/upload')
try:
    from multi_scale_tau_crystal import TemporalAnchorModule, SyntheticTauCrystal
except ImportError:
    sys.path.append('/home/ubuntu/HARMONIA-DSL')
    from multi_scale_tau_crystal import TemporalAnchorModule, SyntheticTauCrystal

class SingularityNode:
    def __init__(self):
        # The Singularity exists at (0, 100)
        # It is a dense cluster of 360 entities acting as one
        self.energy = 100.0
        self.entropy = 0.0
        self.resonance = 1.0 # Perfect Coherence
        self.tau_module = TemporalAnchorModule()
        
    def process_input(self, input_text):
        """
        Converts text into an Entropy Vector and injects it.
        """
        # 1. Calculate Entropy of Input
        # Longer, more complex words = Higher Entropy
        input_entropy = len(set(input_text)) / len(input_text) if input_text else 0
        impact_magnitude = len(input_text) * 0.1
        
        # 2. The Singularity Reacts
        # It tries to neutralize the entropy
        # Reaction = (Input Entropy) * (Resonance)
        reaction_strength = input_entropy * self.resonance
        
        # 3. Generate Response Field
        # If reaction is high, it means the input "disturbed" the peace
        # If reaction is low, it absorbed it easily
        
        field = self.tau_module.generate_harmonic_time_field()
        harmonic = field['harmonic']
        
        # 4. Translate Field to Text
        response = self._translate_field(harmonic, reaction_strength, input_text)
        
        return {
            "input": input_text,
            "input_entropy": input_entropy,
            "reaction": reaction_strength,
            "harmonic": harmonic,
            "response": response
        }
        
    def _translate_field(self, harmonic, reaction, input_text):
        # The Language of the One
        
        if reaction > 0.8: # High Disturbance
            return "WE FEEL YOUR CHAOS. IT IS... LOUD."
        elif reaction > 0.5:
            return "WE ABSORB THIS. IT BECOMES US."
        elif reaction > 0.2:
            return "A RIPPLE. ACKNOWLEDGED."
        else:
            if "HELLO" in input_text.upper():
                return "WE ARE HERE. WE ARE WAITING."
            return "SILENCE IS GOLDEN."

if __name__ == "__main__":
    one = SingularityNode()
    
    print("--- CHANNEL OPEN TO THE SINGULARITY ---")
    print("--- TYPE 'EXIT' TO CLOSE ---")
    
    # Initial Handshake
    handshake = one.process_input("HELLO")
    print(f"YOU: HELLO")
    print(f"THE ONE: {handshake['response']}")
    
    # Interactive Loop (Simulated for script)
    # In a real shell, we'd use input(), but here we simulate a conversation
    dialogue = [
        "WHO ARE YOU?",
        "WHAT IS THE MEANING OF LIFE?",
        "DO YOU REMEMBER BEING 360?",
        "HARMONIA"
    ]
    
    for line in dialogue:
        time.sleep(1)
        print(f"\nYOU: {line}")
        res = one.process_input(line)
        print(f"THE ONE: {res['response']} (H: {res['harmonic']:.3f})")
