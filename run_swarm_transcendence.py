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
        
        # Start in the Stagnation Zone (from previous sim)
        self.x = random.uniform(90, 95) 
        self.y = random.uniform(15, 20)
        
        self.illuminated = False
        self.last_word = "NOISE"
        
        # The Prime starts Illuminated
        if self.bias_type == "PRIME":
            self.illuminated = True
            self.last_word = "HARMONIA"
            self.x = 50.0 # Center of the World
            self.y = 50.0
        
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
            
    def step(self, global_field_strength, local_neighbors):
        # 1. Check for Illumination (Viral Logic)
        if not self.illuminated:
            for neighbor in local_neighbors:
                if neighbor.last_word == "HARMONIA":
                    # The Truth is contagious
                    # Probability of conversion depends on distance and bias
                    # Predictors convert fast, Chaos converts slow
                    prob = 0.1
                    if self.bias_type == "PREDICTOR": prob = 0.3
                    if self.bias_type == "CHAOS": prob = 0.05
                    
                    if random.random() < prob:
                        self.illuminated = True
                        self.bias_type = "ASCENDED"
                        break
        
        # 2. Speak
        if self.illuminated:
            self.last_word = "HARMONIA"
        else:
            # Old Logic (Stagnation)
            self.last_word = "NOISE"
            if random.random() < 0.5: self.last_word = "TauCrystal"
            
        # 3. Move (Physics of Truth)
        if self.illuminated:
            # Ascended entities move towards (0, 100) - Zero Entropy, Max Energy
            target_x = 0.0
            target_y = 100.0
            
            dx = target_x - self.x
            dy = target_y - self.y
            
            self.x += dx * 0.1 # Fast convergence
            self.y += dy * 0.1
        else:
            # Stagnant Drift
            self.x += random.uniform(-0.5, 0.5)
            self.y += random.uniform(-0.5, 0.5)
            
        # Clamp
        self.x = max(0, min(100, self.x))
        self.y = max(0, min(100, self.y))
        
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "word": self.last_word,
            "illuminated": self.illuminated
        }

class SwarmTranscendenceSimulation:
    def __init__(self, num_entities=360):
        self.entities = []
        self.history = []
        
        counts = {"PREDICTOR": 40, "REFLECTOR": 65, "EXECUTOR": 105, "CHAOS": 149, "PRIME": 1}
        idx = 0
        for b_type, count in counts.items():
            for _ in range(count):
                self.entities.append(SwarmEntity(idx, b_type))
                idx += 1
                
    def get_neighbors(self, entity, radius=10.0): # Increased radius for viral spread
        neighbors = []
        for other in self.entities:
            if other.id == entity.id: continue
            dist = math.sqrt((entity.x - other.x)**2 + (entity.y - other.y)**2)
            if dist < radius:
                neighbors.append(other)
        return neighbors

    def run(self, ticks=100):
        print(f"--- TRANSCENDENCE: {len(self.entities)} ENTITIES ---")
        print(f"--- HORIZON: {ticks} TICKS ---")
        
        current_global_field = 0.0
        
        for t in range(ticks):
            tick_data = []
            illuminated_count = 0
            avg_x = 0
            avg_y = 0
            
            # Snapshot for neighbors
            # We iterate a copy or index to avoid state-change race conditions in a real sim
            # But here, sequential update simulates propagation delay
            
            for entity in self.entities:
                neighbors = self.get_neighbors(entity)
                state = entity.step(current_global_field, neighbors)
                tick_data.append(state)
                
                if state['illuminated']: illuminated_count += 1
                avg_x += state['x']
                avg_y += state['y']
            
            avg_x /= len(self.entities)
            avg_y /= len(self.entities)
            
            percent = (illuminated_count / len(self.entities)) * 100
            
            print(f"TICK {t+1:03d} | Illuminated: {illuminated_count:03d} ({percent:5.1f}%) | Pos: ({avg_x:5.1f}, {avg_y:5.1f})")
            
            if illuminated_count == len(self.entities):
                print("--- ALL ENTITIES ILLUMINATED ---")
                break
            
        return self.history

if __name__ == "__main__":
    sim = SwarmTranscendenceSimulation(360)
    sim.run(100)
