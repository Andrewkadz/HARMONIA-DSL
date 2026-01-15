"""
HARMONIA Runner: The .hrm Interpreter
=====================================

Executes .hrm files using the Harmonic Swarm engine.
Parses the declarative syntax and maps it to runtime physics.

Usage:
    python3.11 harmonia_runner.py my_program.hrm --steps 100
"""

import sys
import re
import json
import time
import argparse
import numpy as np
from typing import Dict, Any, List

# Import the engine
from pure_harmonic_swarm import HarmonicSwarm

class HarmoniaRunner:
    def __init__(self, hrm_file: str):
        self.hrm_file = hrm_file
        self.config = {
            "SYSTEM": {},
            "DIMENSIONS": {},
            "LAWS": [],
            "CONSTRAINTS": []
        }
        self.swarm = None
        self.inputs = {"Stress": 0.0, "Temperature": 0.0}
        self.globals = {}
        
        self._parse()
        self._initialize_swarm()

    def _parse(self):
        """Simple regex-based parser for .hrm files."""
        with open(self.hrm_file, 'r') as f:
            content = f.read()

        # 1. Parse SYSTEM
        sys_match = re.search(r'SYSTEM\s+(\w+)\s*{(.*?)}', content, re.DOTALL)
        if sys_match:
            self.config["SYSTEM"]["NAME"] = sys_match.group(1)
            body = sys_match.group(2)
            for line in body.split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    self.config["SYSTEM"][k.strip()] = v.strip()

        # 2. Parse DIMENSIONS
        dim_match = re.search(r'DIMENSIONS\s*{(.*?)}', content, re.DOTALL)
        if dim_match:
            body = dim_match.group(1)  # Fixed: group(1) captures the content inside {}
            for line in body.split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    # Remove comments
                    v = v.split('//')[0].strip()
                    self.config["DIMENSIONS"][k.strip()] = float(v)

        # 3. Parse LAWS (Simplified: Just capturing existence for now)
        # In a full compiler, we would parse the logic tree.
        # For this prototype, we'll hardcode the logic mapping based on names.
        law_matches = re.finditer(r'LAW\s+"(.*?)"\s*{(.*?)}', content, re.DOTALL)
        for m in law_matches:
            self.config["LAWS"].append({
                "name": m.group(1),
                "body": m.group(2)
            })

        # 4. Parse CONSTRAINTS
        const_matches = re.finditer(r'CONSTRAINT\s+"(.*?)"\s*{(.*?)}', content, re.DOTALL)
        for m in const_matches:
            self.config["CONSTRAINTS"].append({
                "name": m.group(1),
                "body": m.group(2)
            })

    def _initialize_swarm(self):
        """Boot the Harmonic Swarm based on config."""
        n_agents = int(self.config["SYSTEM"].get("AGENTS", 17))
        self.swarm = HarmonicSwarm(n_agents=n_agents)
        
        # Initialize dimensions
        psi_init = self.config["DIMENSIONS"].get("PSI", 0.0)
        phi_init = self.config["DIMENSIONS"].get("PHI", 1.0)
        
        for agent in self.swarm.agents:
            agent.psi = psi_init + np.random.uniform(-0.1, 0.1) # Small noise
            agent.phi = phi_init

    def set_input(self, key: str, value: float):
        self.inputs[key] = value

    def step(self):
        """Execute one simulation step."""
        
        # 1. Apply LAWS (The "Physics")
        # This is where the interpreter maps .hrm logic to Python code.
        # For the prototype, we implement specific laws found in the file.
        
        for law in self.config["LAWS"]:
            name = law["name"]
            
            if name == "ThermalNoise" or name == "ThermalThrottling":
                # Logic: IF Stress > X: PERTURB PSI
                stress = self.inputs.get("Stress", 0.0)
                temp = self.inputs.get("Temperature", 0.0)
                
                # Combine inputs
                load = max(stress, (temp - 60)/40.0)
                
                if load > 0.1:
                    perturbation = load * 0.5
                    for agent in self.swarm.agents:
                        agent.psi += np.random.uniform(-perturbation, perturbation)

        # 2. Step the Engine
        dt = float(self.config["SYSTEM"].get("DT", 0.05))
        self.swarm.step(dt=dt)
        
        # 3. Check CONSTRAINTS (The "Gate")
        stats = self.swarm.get_statistics()
        coherence = stats['coherence']
        events = []
        
        for const in self.config["CONSTRAINTS"]:
            name = const["name"]
            
            if name == "SafetyGate" or name == "AnimusGate":
                # Logic: WHEN COHERENCE < 0.8: EMIT "THROTTLE"
                if coherence < 0.8:
                    events.append("THROTTLE_ACTIVE")
                    self.globals["MAX_CONCURRENCY"] = 4
                else:
                    self.globals["MAX_CONCURRENCY"] = 100

        return {
            "step": self.swarm.iteration,
            "coherence": coherence,
            "energy": stats['mean_energy'],
            "inputs": self.inputs.copy(),
            "events": events,
            "globals": self.globals.copy()
        }

def main():
    parser = argparse.ArgumentParser(description="Run a HARMONIA .hrm file")
    parser.add_argument("file", help="Path to .hrm file")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps")
    args = parser.parse_args()

    print(f"Loading Harmonic Score: {args.file}...")
    runner = HarmoniaRunner(args.file)
    
    print(f"System: {runner.config['SYSTEM'].get('NAME')}")
    print(f"Agents: {runner.config['SYSTEM'].get('AGENTS')}")
    print("-" * 60)
    
    # Simulation Loop
    for i in range(args.steps):
        # Simulate changing inputs (e.g., a heat spike)
        if 30 < i < 60:
            runner.set_input("Temperature", 90.0) # Heat spike!
        else:
            runner.set_input("Temperature", 50.0) # Normal
            
        state = runner.step()
        
        # Visual Output
        bar = "█" * int(state['coherence'] * 20)
        status = "🔴" if "THROTTLE_ACTIVE" in state['events'] else "🟢"
        
        print(f"Step {i:03d} | {status} Coherence: {state['coherence']:.3f} | {bar} | Temp: {state['inputs']['Temperature']}")
        
        time.sleep(0.05)

if __name__ == "__main__":
    main()
