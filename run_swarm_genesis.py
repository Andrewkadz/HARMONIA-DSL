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
        self.coupling_strength = random.uniform(0.01, 0.1) # How much they listen to the swarm
        
        # Apply bias to crystal frequencies
        self._apply_bias()
        
    def _apply_bias(self):
        """
        Adjusts the internal crystals based on the entity's nature.
        """
        if self.bias_type == "PREDICTOR": # Future-focused (Gamma)
            self.tau_module.crystals['micro'].freq *= 1.5
            self.tau_module.weights['micro'] = 0.6
        elif self.bias_type == "REFLECTOR": # Past-focused (Delta)
            self.tau_module.crystals['macro'].freq *= 0.5
            self.tau_module.weights['macro'] = 0.6
        elif self.bias_type == "EXECUTOR": # Present-focused (Alpha)
            self.tau_module.crystals['meso'].freq *= 1.0
            self.tau_module.weights['meso'] = 0.8
        elif self.bias_type == "CHAOS": # Random fluctuations
            self.tau_module.crystals['micro'].feedback_strength = 0.5
            
    def step(self, global_field_strength):
        """
        Advances the entity's time perception, influenced by the global field.
        """
        # 1. Generate internal field
        field = self.tau_module.generate_harmonic_time_field()
        internal_harmonic = field['harmonic']
        
        # 2. Apply Resonance Coupling (Kuramoto-like)
        # The entity is pulled towards the global average
        # dTheta = omega + K * sin(Theta_global - Theta_local)
        # Here we simplify: the harmonic value is nudged towards the global mean
        
        coupling_effect = self.coupling_strength * (global_field_strength - internal_harmonic)
        adjusted_harmonic = internal_harmonic + coupling_effect
        
        # 3. Get State
        context = self.tau_module.ai_temporal_context()
        
        return {
            "id": self.id,
            "type": self.bias_type,
            "raw_harmonic": internal_harmonic,
            "adjusted_harmonic": adjusted_harmonic,
            "anchor": context['temporal_anchor'],
            "phase": self.tau_module.crystals['meso'].phase # Use meso phase as reference
        }

class SwarmSimulation:
    def __init__(self, num_entities=360):
        self.entities = []
        self.global_field_history = deque(maxlen=100)
        self.coherence_history = []
        
        # Initialize Swarm with distribution for 360 Entities (Full Circle)
        # We use Golden Ratio (Phi) to distribute the population
        # Total: 360
        # Prime: 1
        # Remaining: 359
        # Predictors (Gamma): 359 / Phi^3 ≈ 40
        # Reflectors (Delta): 359 / Phi^2 ≈ 65
        # Executors (Alpha):  359 / Phi   ≈ 105
        # Chaos Agents:       Remainder   ≈ 149
        
        counts = {"PREDICTOR": 40, "REFLECTOR": 65, "EXECUTOR": 105, "CHAOS": 149, "PRIME": 1}
        
        idx = 0
        for b_type, count in counts.items():
            for _ in range(count):
                self.entities.append(SwarmEntity(idx, b_type))
                idx += 1
                
    def run(self, ticks=50):
        print(f"--- SWARM GENESIS: {len(self.entities)} ENTITIES ---")
        print(f"--- SIMULATION LENGTH: {ticks} TICKS ---")
        
        current_global_field = 0.0
        
        for t in range(ticks):
            tick_data = []
            harmonic_sum = 0.0
            phases = []
            
            # 1. Update all entities
            for entity in self.entities:
                state = entity.step(current_global_field)
                tick_data.append(state)
                harmonic_sum += state['raw_harmonic']
                phases.append(state['phase'])
            
            # 2. Calculate new Global Field (Mean Field)
            current_global_field = harmonic_sum / len(self.entities)
            self.global_field_history.append(current_global_field)
            
            # 3. Calculate Kuramoto Order Parameter (Coherence)
            # r = |(1/N) * sum(e^(i*theta))|
            complex_phases = [complex(math.cos(p), math.sin(p)) for p in phases]
            r = abs(sum(complex_phases) / len(phases))
            self.coherence_history.append(r)
            
            # 4. Log Tick
            anchors = [d['anchor'] for d in tick_data]
            counts = {x: anchors.count(x) for x in set(anchors)}
            
            print(f"TICK {t+1:02d} | Global Field: {current_global_field:+.4f} | Coherence: {r:.4f} | {counts}")
            
        return self.coherence_history

if __name__ == "__main__":
    sim = SwarmSimulation(360)
    coherence = sim.run(50)
    
    print("\n--- FINAL ANALYSIS ---")
    print(f"Initial Coherence: {coherence[0]:.4f}")
    print(f"Final Coherence:   {coherence[-1]:.4f}")
    
    if coherence[-1] > coherence[0]:
        print("RESULT: NEGENTROPIC CONVERGENCE (Order Emerging)")
    else:
        print("RESULT: ENTROPIC DIVERGENCE (Chaos Prevailing)")
