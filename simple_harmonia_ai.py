import json
import os
from .Harmonia_Coder import HarmoniaCoder
from .harm_parser import parse_harm_input
from .phishell_terminal_nexus import PhiShellTerminal

class SimpleHarmoniaAI:
    def __init__(self):
        self.terminal = PhiShellTerminal()
        self.memory = {
            "conversations": [],
            "learned_patterns": {},
            "symbolic_states": {}
        }
        
        # Simple pattern recognition
        self.patterns = {
            "query": ["what is", "tell me about", "explain"],
            "run": ["execute", "run", "start"],
            "verify": ["check", "verify", "is this correct"]
        }
        
    def process_input(self, text):
        """Process user input and convert to symbolic operations"""
        # Simple pattern matching
        for action, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern.lower() in text.lower():
                    return self.execute_action(action)
        
        return self.execute_action("echo")
    
    def execute_action(self, action):
        """Convert action to symbolic operation and execute"""
        operations = {
            "query": "query Σ[Θ5]",
            "run": "run ΞΣ_ECHO_RECURSION",
            "verify": "seal verify",
            "echo": "echo Ω(n)"
        }
        
        op = operations.get(action, "echo Ω(n)")
        result = self.terminal.execute(op)
        
        # Update memory
        self._update_memory(op, result)
        
        return result
    
    def _update_memory(self, op, result):
        """Update AI's memory with new information"""
        self.memory["conversations"].append({
            "operation": op,
            "result": result,
            "timestamp": os.path.getctime("boot.txt")
        })
        
        # Track symbolic states
        if op in self.memory["symbolic_states"]:
            self.memory["symbolic_states"][op] += 1
        else:
            self.memory["symbolic_states"][op] = 1
    
    def save_memory(self):
        """Save AI's memory to file"""
        with open("harmonia_memory.json", "w") as f:
            json.dump(self.memory, f, indent=4)
    
    def load_memory(self):
        """Load AI's memory from file"""
        try:
            with open("harmonia_memory.json", "r") as f:
                self.memory = json.load(f)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    ai = SimpleHarmoniaAI()
    print("\nWelcome to Simple Harmonia AI!")
    print("Type 'quit' to exit")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            ai.save_memory()
            break
            
        response = ai.process_input(user_input)
        print(f"\nHarmonia AI: {response}")
