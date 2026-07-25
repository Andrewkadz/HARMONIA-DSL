import numpy as np

class SwarmHomeostasis:
    def __init__(self):
        self.stress_level = 0.0
        self.adaptation_rate = 0.05
        self.resilience = 1.0
        self.trauma_history = []
        
    def evaluate_state(self, coherence, entropy, energy_input):
        """
        The Swarm 'feels' its state.
        High Energy + Low Coherence = High Stress (Panic)
        High Energy + High Coherence = Flow (Eustress)
        """
        # Calculate Stress
        # Stress increases if Input Energy is high but Coherence is low
        # It decreases if Coherence is high
        
        current_stress = (energy_input * (1.0 - coherence))
        
        # Smooth the stress response (biological lag)
        self.stress_level = (self.stress_level * 0.9) + (current_stress * 0.1)
        
        return self.stress_level
        
    def adapt(self, stress):
        """
        The Swarm chooses a strategy based on stress.
        Returns a 'Plasticity Factor' (how much to change its own parameters).
        """
        if stress > 0.8:
            # CRITICAL STATE: The Swarm is overwhelmed.
            # Strategy: YIELD (High Plasticity). Let the structure melt to survive.
            # "Be like water."
            self.trauma_history.append("COLLAPSE_AVOIDANCE")
            return 2.0 # Double the fluidity
            
        elif stress > 0.5:
            # ALERT STATE: The Swarm is under load.
            # Strategy: BRACE (Low Plasticity). Hold the line.
            return 0.5 # Stiffen up
            
        else:
            # REST STATE: Recovery.
            # Strategy: GROW (Normal Plasticity).
            return 1.0
            
    def learn_from_trauma(self):
        """
        If the Swarm survived a collapse, it gains Resilience.
        """
        if len(self.trauma_history) > 0:
            # What doesn't kill it makes it stronger
            self.resilience += 0.01
            # Clear history after learning
            self.trauma_history = []
            
        return self.resilience
