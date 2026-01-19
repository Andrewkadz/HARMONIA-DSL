import numpy as np
import json
import time

class TauCrystal:
    def __init__(self, id, state_vector, coherence, timestamp):
        self.id = id
        self.state_vector = state_vector  # The Quantum State (Complex Vector)
        self.coherence = coherence
        self.timestamp = timestamp
        self.energy = 1.0  # Decay factor (crystals fade if not reinforced)

class TauMemoryField:
    def __init__(self, capacity=10):
        self.crystals = []
        self.capacity = capacity
        self.resonance_threshold = 0.8  # Similarity needed to trigger resonance
        
    def crystallize(self, current_state, coherence):
        """
        Attempt to form a new Tau Crystal from the current state.
        Only forms if Coherence is high and state is unique.
        """
        # 1. Check Uniqueness (Don't store duplicates)
        for crystal in self.crystals:
            similarity = self._calculate_fidelity(current_state, crystal.state_vector)
            if similarity > 0.95:
                # Reinforce existing crystal instead of creating new one
                crystal.energy = min(crystal.energy + 0.2, 2.0)
                return None
                
        # 2. Create New Crystal
        new_id = f"TAU_{int(time.time())}_{len(self.crystals)}"
        new_crystal = TauCrystal(new_id, np.copy(current_state), coherence, time.time())
        
        self.crystals.append(new_crystal)
        
        # 3. Prune Weakest if over capacity
        if len(self.crystals) > self.capacity:
            self.crystals.sort(key=lambda x: x.energy * x.coherence, reverse=True)
            self.crystals.pop() # Remove last
            
        return new_id

    def get_temporal_gravity(self, current_state):
        """
        Calculate the 'Pull' of past crystals on the current state.
        Returns a Force Vector (Delta State) to nudge the system.
        """
        if not self.crystals:
            return np.zeros_like(current_state)
            
        total_pull = np.zeros_like(current_state)
        
        for crystal in self.crystals:
            # Calculate Quantum Fidelity (Similarity)
            # F = |<psi|phi>|^2
            fidelity = self._calculate_fidelity(current_state, crystal.state_vector)
            
            # Resonance Logic:
            # If we are "close" (fidelity > threshold), the crystal pulls us closer.
            # Pull Strength = Fidelity * Crystal Energy
            if fidelity > self.resonance_threshold:
                # Direction: Towards the Crystal State
                # Vector difference in Hilbert Space
                direction = crystal.state_vector - current_state
                pull = direction * fidelity * crystal.energy * 0.1 # 0.1 is coupling constant
                total_pull += pull
                
        return total_pull

    def _calculate_fidelity(self, state_a, state_b):
        """
        Compute Quantum Fidelity between two state vectors.
        """
        # Inner product
        overlap = np.vdot(state_a, state_b)
        return np.abs(overlap)**2

    def decay(self):
        """
        Apply entropy to memory (crystals fade over time).
        """
        for crystal in self.crystals:
            crystal.energy *= 0.995 # Slow decay
