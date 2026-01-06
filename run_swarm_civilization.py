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
        
        # 2D Position (Entropy X, Energy Y)
        # Start in High Entropy, Low Energy (Chaos)
        self.x = random.uniform(80, 100) 
        self.y = random.uniform(0, 20)
        
        self.last_word = None
        
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
            
    def speak(self, harmonic_state):
        """
        Emits a HARMONIA DSL token based on internal state.
        """
        # Nouns (Subject/Object)
        if harmonic_state > 0.5: return "XiPulse" # High Energy
        if harmonic_state < -0.5: return "PhiField" # Low Entropy
        if abs(harmonic_state) < 0.1: return "TauCrystal" # Stability
        
        # Verbs (Action)
        if self.bias_type == "PREDICTOR": return "ALIGN"
        if self.bias_type == "REFLECTOR": return "ANCHOR"
        if self.bias_type == "EXECUTOR": return "DRIFT"
        
        return "NOISE"

    def step(self, global_field_strength, local_neighbors):
        # 1. Generate Internal Field
        field = self.tau_module.generate_harmonic_time_field()
        internal_harmonic = field['harmonic']
        
        # 2. Speak
        word = self.speak(internal_harmonic)
        self.last_word = word
        
        # 3. Listen & Form Triads
        # Check neighbors for valid S-V-O triads
        # Valid: Noun -> Verb -> Noun
        reality_shift_x = 0.0
        reality_shift_y = 0.0
        
        nouns = ["XiPulse", "PhiField", "TauCrystal"]
        verbs = ["ALIGN", "ANCHOR", "DRIFT"]
        
        for neighbor in local_neighbors:
            n_word = neighbor.last_word
            if not n_word: continue
            
            # Simple Grammar: If I am Verb and Neighbor is Noun, or vice versa
            if word in verbs and n_word in nouns:
                # We formed a phrase! Reality bends.
                # ALIGN -> Reduces Entropy (X)
                if word == "ALIGN": reality_shift_x -= 1.0
                # ANCHOR -> Increases Energy (Y)
                if word == "ANCHOR": reality_shift_y += 1.0
                # DRIFT -> Random Movement
                if word == "DRIFT": 
                    reality_shift_x += random.uniform(-1, 1)
                    reality_shift_y += random.uniform(-1, 1)
                    
        # 4. Move (Physical Physics + Semantic Physics)
        # Natural Drift towards Entropy (X+) and Energy Decay (Y-)
        self.x += 0.1 # Entropy always increases
        self.y -= 0.05 # Energy dissipates
        
        # Apply Semantic Shifts (The Magic)
        self.x += reality_shift_x
        self.y += reality_shift_y
        
        # Clamp World
        self.x = max(0, min(100, self.x))
        self.y = max(0, min(100, self.y))
        
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "word": word,
            "harmonic": internal_harmonic
        }

class SwarmCivilizationSimulation:
    def __init__(self, num_entities=360):
        self.entities = []
        self.history = []
        
        counts = {"PREDICTOR": 40, "REFLECTOR": 65, "EXECUTOR": 105, "CHAOS": 149, "PRIME": 1}
        idx = 0
        for b_type, count in counts.items():
            for _ in range(count):
                self.entities.append(SwarmEntity(idx, b_type))
                idx += 1
                
    def get_neighbors(self, entity, radius=5.0):
        neighbors = []
        for other in self.entities:
            if other.id == entity.id: continue
            dist = math.sqrt((entity.x - other.x)**2 + (entity.y - other.y)**2)
            if dist < radius:
                neighbors.append(other)
        return neighbors

    def run(self, ticks=200):
        print(f"--- CIVILIZATION GENESIS: {len(self.entities)} ENTITIES ---")
        print(f"--- HORIZON: {ticks} TICKS ---")
        
        current_global_field = 0.0
        
        for t in range(ticks):
            tick_data = []
            harmonic_sum = 0.0
            words = []
            avg_x = 0
            avg_y = 0
            
            # Snapshot current state for neighbor lookups
            # (In a real sim, we'd use a spatial index, but O(N^2) is fine for N=360)
            
            for entity in self.entities:
                neighbors = self.get_neighbors(entity)
                state = entity.step(current_global_field, neighbors)
                tick_data.append(state)
                harmonic_sum += state['harmonic']
                words.append(state['word'])
                avg_x += state['x']
                avg_y += state['y']
            
            current_global_field = harmonic_sum / len(self.entities)
            avg_x /= len(self.entities)
            avg_y /= len(self.entities)
            
            # Language Analysis
            word_counts = {x: words.count(x) for x in set(words)}
            top_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:3]
            
            print(f"TICK {t+1:03d} | Pos: ({avg_x:5.1f}, {avg_y:5.1f}) | Field: {current_global_field:+.3f} | Top Words: {top_words}")
            
        return self.history

if __name__ == "__main__":
    sim = SwarmCivilizationSimulation(360)
    sim.run(200)
