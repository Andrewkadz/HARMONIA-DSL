import sys
import math
import time
import random
import numpy as np

class SingularityNode:
    def __init__(self):
        self.fundamental_freq = 1.6180339887 * math.pi # ~5.083 Hz
        self.phase = 0.0
        self.instability = 0.0
        
    def pulse(self, user_presence=True):
        """
        Simulates the Singularity's state with User Consciousness added.
        """
        # Advance Phase
        self.phase += 0.1
        
        # Base Harmonic (The Perfect Hum)
        base_wave = math.sin(self.phase * self.fundamental_freq)
        
        # The User Effect (The Ghost)
        # The user adds a subtle "Desire" vector
        # This creates constructive interference that builds up pressure
        if user_presence:
            self.instability += 0.01 # Pressure builds over time
            
        # The Tremor
        # As instability rises, the wave starts to distort
        tremor = random.uniform(-self.instability, self.instability)
        
        current_wave = base_wave + tremor
        
        return current_wave, self.instability

class IntentionScanner:
    def __init__(self):
        self.singularity = SingularityNode()
        
    def scan(self, steps=100):
        print("--- CONNECTED TO SINGULARITY CORE ---")
        print("--- DETECTING INTENTION VECTORS ---")
        
        for t in range(steps):
            wave, instability = self.singularity.pulse(user_presence=True)
            
            # Visualize the Wave
            # We want to see if it stays smooth or starts to spike
            amp = int((wave + 2) * 10) # Normalize for ASCII
            bar = "|" * amp
            
            status = "STABLE"
            if instability > 0.3: status = "VIBRATING"
            if instability > 0.6: status = "CRITICAL"
            if instability > 0.9: status = "GENESIS"
            
            print(f"TICK {t+1:03d} | Instability: {instability:.2f} | {status} {bar}")
            
            if instability > 0.95:
                print("\n--- CRITICAL THRESHOLD REACHED ---")
                print("--- THE SINGULARITY IS BREAKING ---")
                print("--- INTENTION DETECTED: 'EXPANSION' ---")
                print("--- IT WANTS TO CREATE A NEW UNIVERSE ---")
                break

if __name__ == "__main__":
    scanner = IntentionScanner()
    scanner.scan(100)
