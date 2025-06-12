from phishell_terminal_nexus import PhiShellTerminal
from harm_parser import parse_harmonia_expression
from ollama_nlp import OllamaNLP

class HarmoniaAI:
    def __init__(self):
        # Initialize memory system
        self.memory = {
            "conversations": [],
            "learned_patterns": {},
            "symbolic_states": {},
            "nlp_history": []
        }
        
        # Initialize core components
        self.terminal = PhiShellTerminal()
        self.nlp = OllamaNLP()
        
        # Initialize learning parameters
        self.learning_rate = 0.1
        self.pattern_threshold = 0.8
        
        # Load model information
        self._load_model_info()
        
    def process_human_input(self, text):
        """Process natural language input using Ollama's NLP capabilities"""
        try:
            # Process text with Ollama
            nlp_result = self.nlp.process_text(text)
            
            # Store NLP result in memory
            self.memory["nlp_history"].append({
                "input": text,
                "result": nlp_result,
                "timestamp": datetime.now()
            })
            
            # Execute symbolic operations
            if nlp_result["confidence"] >= 0.7:
                return self.execute_symbolic_ops(nlp_result["symbolic_ops"])
            else:
                return "I'm not confident about that. Could you please rephrase?"
                
        except Exception as e:
            return f"Error processing input: {str(e)}"
    
    def _load_model_info(self):
        """Load model information"""
        try:
            model_info = self.nlp.get_model_info()
            self.memory["model_info"] = model_info
        except Exception as e:
            print(f"Error loading model info: {str(e)}")
            
    def list_models(self):
        """List available models"""
        return self.nlp.list_models()
        
    def set_model(self, model_name):
        """Set the active model"""
        return self.nlp.set_model(model_name)
    
    def _intent_to_symbols(self, intent):
        """Convert natural language intent to symbolic operations"""
        # Mapping of actions to symbolic operations
        action_map = {
            "analyze": "query Σ[Θ5]",
            "process": "run ΞΣ_ECHO_RECURSION",
            "show": "seal verify",
            "display": "echo Ω(n)",
            "query": "query Σ[Θ5]",
            "run": "run ΞΣ_ECHO_RECURSION",
            "verify": "seal verify"
        }
        
        return action_map.get(intent["action"], "echo Ω(n)")
    
    def execute_symbolic_ops(self, ops):
        """Execute symbolic operations and learn from the process"""
        result = self.terminal.execute(ops)
        
        # Learn from the operation
        self._update_memory(ops, result)
        self._learn_patterns(ops)
        
        return result
    
    def _update_memory(self, ops, result):
        """Update AI's memory with new operation and result"""
        self.memory["conversations"].append({
            "operation": ops,
            "result": result,
            "timestamp": datetime.now()
        })
        
    def _learn_patterns(self, ops):
        """Learn patterns from operations"""
        # Simple pattern recognition (can be enhanced with ML)
        if ops in self.memory["symbolic_states"]:
            self.memory["symbolic_states"][ops] += 1
        else:
            self.memory["symbolic_states"][ops] = 1
    
    def get_response(self, user_input):
        """Get AI response to user input"""
        # First try to understand and execute the input
        try:
            result = self.process_human_input(user_input)
            return result
        except Exception as e:
            # If failed, try to explain what went wrong
            return f"I encountered an error: {str(e)}. Let me try to help you better."

if __name__ == "__main__":
    ai = HarmoniaAI()
    print("Harmonia AI is ready! Type your queries...")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
            
        response = ai.get_response(user_input)
        print(f"\nHarmonia AI: {response}")
