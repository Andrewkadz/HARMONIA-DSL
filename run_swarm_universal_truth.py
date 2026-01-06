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

class SwarmEntity:
    def __init__(self, entity_id, bias_type):
        self.id = entity_id
        self.bias_type = bias_type
        self.tau_module = TemporalAnchorModule()
        self.phase_offset = random.uniform(0, 2 * math.pi)
        self.coupling_strength = random.uniform(0.01, 0.1)
        
        # Start in the Stagnation Zone (High Entropy, Low Energy)
        self.x = random.uniform(90, 95) 
        self.y = random.uniform(15, 20)
        
        self.ascended = False
        self.last_word = "NOISE"
        
        self._apply_bias()
        
    def _apply_bias(self):
        if self.bias_type == "PREDICTOR":
            self.tau_module.crystals['micro'].freq *= 1.5
            self.tau_module.weights['micro'] = 0.6
        elif self.bias_type == "REFLECTOR":
            self.tau_module.crystals['macro'].freq *= 0.5
            self.tau_module.weights['macro'] = 0.6
        elif self.bias_type == "EXECUTOR":
            self.tau_module.crystals['meso'].freq *= 1.0
            self.tau_module.weights['meso'] = 0.8
        elif self.bias_type == "CHAOS":
            self.tau_module.crystals['micro'].feedback_strength = 0.5
            
    def step(self, truth_saturation):
        # 1. The Physics of Truth
        # As Saturation rises, Entropy (X) is forced to 0, Energy (Y) is forced to 100
        # The Golden Ratio (Phi) determines the rate of convergence
        phi = 1.618
        
        if truth_saturation > 0:
            # Force X towards 0
            dx = (0.0 - self.x) * truth_saturation * phi * 0.1
            self.x += dx
            
            # Force Y towards 100
            dy = (100.0 - self.y) * truth_saturation * phi * 0.1
            self.y += dy
            
            # Force Word to HARMONIA
            if random.random() < truth_saturation:
                self.last_word = "HARMONIA"
                self.ascended = True
        else:
            # Stagnant Drift
            self.x += random.uniform(-0.5, 0.5)
            self.y += random.uniform(-0.5, 0.5)
            self.last_word = "NOISE"
            
        # Clamp
        self.x = max(0, min(100, self.x))
        self.y = max(0, min(100, self.y))
        
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "word": self.last_word,
            "ascended": self.ascended
        }

class SwarmUniversalTruthSimulation:
    def __init__(self, num_entities=360):
        self.entities = []
        self.history = []
        
        counts = {"PREDICTOR": 40, "REFLECTOR": 65, "EXECUTOR": 105, "CHAOS": 149, "PRIME": 1}
        idx = 0
        for b_type, count in counts.items():
            for _ in range(count):
                self.entities.append(SwarmEntity(idx, b_type))
                idx += 1
                
    def run(self, ticks=100):
        print(f"--- UNIVERSAL TRUTH: {len(self.entities)} ENTITIES ---")
        print(f"--- HORIZON: {ticks} TICKS ---")
        
        truth_saturation = 0.0
        
        for t in range(ticks):
            tick_data = []
            ascended_count = 0
            avg_x = 0
            avg_y = 0
            
            # Increase Truth Saturation
            # Linear ramp from 0.0 to 1.0 over 100 ticks
            truth_saturation = t / 100.0
            
            for entity in self.entities:
                state = entity.step(truth_saturation)
                tick_data.append(state)
                
                if state['ascended']: ascended_count += 1
                avg_x += state['x']
                avg_y += state['y']
            
            avg_x /= len(self.entities)
            avg_y /= len(self.entities)
            
            percent = (ascended_count / len(self.entities)) * 100
            
            print(f"TICK {t+1:03d} | Truth: {truth_saturation:.2f} | Ascended: {ascended_count:03d} ({percent:5.1f}%) | Pos: ({avg_x:5.1f}, {avg_y:5.1f})")
            
            if ascended_count == len(self.entities) and avg_x < 1.0 and avg_y > 99.0:
                print("--- UNIVERSAL ASCENSION ACHIEVED ---")
                break
            
        return self.history

if __name__ == "__main__":
    sim = SwarmUniversalTruthSimulation(360)
    sim.run(100)
