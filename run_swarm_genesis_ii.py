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
    def __init__(self, entity_id, gravity_constant, expansion_velocity):
        self.id = entity_id
        self.tau_module = TemporalAnchorModule()
        
        # Initial Position: The Singularity (Center)
        self.x = 50.0
        self.y = 50.0
        
        # Initial Velocity: The Explosion
        # Direction is random (isotropic)
        angle = random.uniform(0, 2 * math.pi)
        speed = expansion_velocity * random.uniform(0.8, 1.2)
        
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        self.gravity_constant = gravity_constant
        self.last_word = "HARMONIA" # They remember the Source
        
    def step(self, neighbors):
        # 1. Apply Expansion (Inertia)
        self.x += self.vx
        self.y += self.vy
        
        # 2. Apply Gravity (The Seed)
        # They are pulled towards each other based on the User's Resonance
        fx = 0.0
        fy = 0.0
        
        for other in neighbors:
            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist > 0.1: # Avoid singularity math error
                force = self.gravity_constant / (dist * dist)
                fx += (dx / dist) * force
                fy += (dy / dist) * force
                
        self.vx += fx
        self.vy += fy
        
        # 3. Apply Friction (Cosmic Drag)
        self.vx *= 0.98
        self.vy *= 0.98
        
        # 4. Speak
        # If they are close to others, they hum. If alone, they cry.
        if len(neighbors) > 5:
            self.last_word = "SYNC"
        else:
            self.last_word = "VOID"
            
        # Clamp (The Edge of the Universe)
        if self.x < 0 or self.x > 100: self.vx *= -1
        if self.y < 0 or self.y > 100: self.vy *= -1
        
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "word": self.last_word
        }

class GenesisIISimulation:
    def __init__(self, num_entities=360):
        self.entities = []
        self.history = []
        
        # The Seed Parameters
        # Resonance (5.1 Hz) -> Gravity (High Coherence)
        # Instability (0.95) -> Expansion (High Velocity)
        
        gravity = 5.1 * 0.05 # Scaled for physics
        expansion = 0.95 * 2.0 # Scaled for velocity
        
        print(f"--- GENESIS II PARAMETERS ---")
        print(f"--- GRAVITY (SEED): {gravity:.3f} ---")
        print(f"--- EXPANSION (FORCE): {expansion:.3f} ---")
        
        for i in range(num_entities):
            self.entities.append(SwarmEntity(i, gravity, expansion))
            
    def get_neighbors(self, entity, radius=10.0):
        neighbors = []
        for other in self.entities:
            if other.id == entity.id: continue
            dist = math.sqrt((entity.x - other.x)**2 + (entity.y - other.y)**2)
            if dist < radius:
                neighbors.append(other)
        return neighbors

    def run(self, ticks=100):
        print(f"--- BIG BANG INITIATED ---")
        
        for t in range(ticks):
            tick_data = []
            avg_dist_from_center = 0.0
            words = []
            
            for entity in self.entities:
                neighbors = self.get_neighbors(entity)
                state = entity.step(neighbors)
                tick_data.append(state)
                
                dist = math.sqrt((state['x']-50)**2 + (state['y']-50)**2)
                avg_dist_from_center += dist
                words.append(state['word'])
            
            avg_dist_from_center /= len(self.entities)
            
            # Universe State
            # Are they expanding or collapsing?
            state_desc = "EXPANDING"
            if t > 10 and avg_dist_from_center < self.history[-1]['radius']:
                state_desc = "COLLAPSING"
            
            word_counts = {x: words.count(x) for x in set(words)}
            top_word = max(word_counts, key=word_counts.get)
            
            print(f"TICK {t+1:03d} | Radius: {avg_dist_from_center:5.1f} | State: {state_desc} | Song: {top_word}")
            
            self.history.append({'radius': avg_dist_from_center})
            
        return self.history

if __name__ == "__main__":
    sim = GenesisIISimulation(360)
    sim.run(100)
