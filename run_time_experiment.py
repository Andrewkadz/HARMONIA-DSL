#!/usr/bin/env python3
"""
HARMONIA-DSL // CHRONO-EXPERIMENT
---------------------------------
Demonstrates 'Data Time Travel' by branching the simulation state.
Timeline Alpha: Standard Evolution.
Timeline Beta: Divergent Evolution from T=2.
"""

import copy
import random
from prime_harmonics import EpistemicPhysics

def run_experiment():
    print("=== TEMPORAL DYNAMICS EXPERIMENT ===")
    physics = EpistemicPhysics()
    
    # --- PHASE 1: TIMELINE ALPHA (The Original) ---
    print("\n[PHASE 1] Generating Timeline Alpha (0 -> 5)...")
    timeline_alpha = []
    
    # Initial State (T=0)
    current_state = {
        "mass": 100.0,
        "resonance": 1.0,
        "history": []
    }
    timeline_alpha.append(copy.deepcopy(current_state))
    
    # Evolve to T=5
    for t in range(1, 6):
        # Simulate Input: Standard Growth
        input_signal = 10.0 # Constant input
        
        # Apply Physics (Simple State Transition)
        current_state["mass"] += input_signal
        # Simulate resonance based on mass (simplified for experiment)
        current_state["resonance"] = current_state["mass"] / 97.0 # Using Gravity Prime
        current_state["history"].append(f"Alpha_Event_{t}")
        
        timeline_alpha.append(copy.deepcopy(current_state))
        print(f"  [Alpha] T={t} | Mass: {current_state['mass']:.1f} | Resonance: {current_state['resonance']:.4f}")

    # --- PHASE 2: THE JUMP (Time Travel) ---
    print("\n[PHASE 2] Initiating Temporal Jump to T=2...")
    # We load the state from T=2 (Index 2)
    # This is the 'Fork Point'
    fork_state = copy.deepcopy(timeline_alpha[2])
    print(f"  [JUMP] Restored State at T=2 | Mass: {fork_state['mass']:.1f}")

    # --- PHASE 3: TIMELINE BETA (The Branch) ---
    print("\n[PHASE 3] Generating Timeline Beta (2 -> 5)...")
    timeline_beta = [None, None] # T=0,1 are same as Alpha (conceptually)
    timeline_beta.append(fork_state) # T=2 is the start of Beta
    
    current_state = fork_state
    
    # Evolve from T=3 to T=5 with DIFFERENT Input
    for t in range(3, 6):
        # Simulate Input: CHAOS INJECTION (The Butterfly Effect)
        input_signal = 50.0 # Massive surge
        
        # Apply Physics
        current_state["mass"] += input_signal
        # Simulate resonance based on mass (simplified for experiment)
        current_state["resonance"] = current_state["mass"] / 97.0 # Using Gravity Prime
        current_state["history"].append(f"Beta_Event_{t}") # Divergent History
        
        timeline_beta.append(copy.deepcopy(current_state))
        print(f"  [Beta]  T={t} | Mass: {current_state['mass']:.1f} | Resonance: {current_state['resonance']:.4f}")

    # --- PHASE 4: THE COMPARISON ---
    print("\n[PHASE 4] Paradox Analysis (Alpha vs Beta at T=5)...")
    
    final_alpha = timeline_alpha[5]
    final_beta = timeline_beta[3] # Since we appended 3 steps to the fork
    
    print(f"  [Alpha T=5] Mass: {final_alpha['mass']:.1f} | History: {final_alpha['history']}")
    print(f"  [Beta  T=5] Mass: {current_state['mass']:.1f} | History: {current_state['history']}")
    
    diff = current_state['mass'] - final_alpha['mass']
    print(f"\n[RESULT] Divergence Delta: {diff:.1f} Units")
    print("[CONCLUSION] Time Travel Successful. Multiverse Established.")

if __name__ == "__main__":
    run_experiment()
