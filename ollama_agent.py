import requests
import json
from ai_agent import AIFileAgent
from harmonia_ai import HarmoniaAI

class OllamaAgent(AIFileAgent):
    def __init__(self):
        super().__init__()
        self.ollama_url = "http://localhost:11434/api"
        self.model = "llama2"
        self.system_prompt = "You are a sophisticated AI assistant for HΛRM OS. You have access to the file system and can analyze patterns. Maintain context and provide accurate responses."
        
        # Initialize Ollama connection
        self._initialize_ollama()
        
    def _initialize_ollama(self):
        """Initialize Ollama connection and check models"""
        try:
            # Check available models
            response = requests.get(f"{self.ollama_url}/tags")
            models = response.json()
            
            # Set default model if available
            if self.model in [m["name"] for m in models["models"]]:
                self._set_model(self.model)
            else:
                print(f"Warning: Model {self.model} not found. Using default model.")
                self._set_model(models["models"][0]["name"])
                
        except Exception as e:
            print(f"Error initializing Ollama: {str(e)}")
            
    def _set_model(self, model_name):
        """Set the active model"""
        self.model = model_name
        self.system_prompt = {
            "role": "system",
            "content": self.system_prompt
        }
        
    def _generate_prompt(self, query, context=None):
        """Generate prompt for Ollama"""
        messages = [self.system_prompt]
        
        # Add context if available
        if context:
            messages.append({
                "role": "user",
                "content": f"Context: {context}"
            })
            
        # Add query
        messages.append({
            "role": "user",
            "content": query
        })
        
        return {
            "model": self.model,
            "messages": messages
        }
        
    def _call_ollama(self, prompt):
        """Call Ollama API"""
        try:
            response = requests.post(
                f"{self.ollama_url}/chat",
                json=prompt
            )
            return response.json()["response"]
        except Exception as e:
            return f"Error calling Ollama: {str(e)}"
            
    def process_query(self, query):
        """Process query using Ollama"""
        # Get context from memory
        context = self._get_context(query)
        
        # Generate prompt
        prompt = self._generate_prompt(query, context)
        
        # Call Ollama
        response = self._call_ollama(prompt)
        
        # Process response
        if isinstance(response, str):
            return self._process_text_response(response)
        else:
            return self._process_structured_response(response)
            
    def _process_text_response(self, text):
        """Process text response from Ollama"""
        # Analyze response
        analysis = self._analyze_response(text)
        
        # Update memory
        self._update_memory(text, analysis)
        
        return {
            "response": text,
            "analysis": analysis,
            "recommendations": self._generate_recommendations(analysis)
        }
        
    def _process_structured_response(self, response):
        """Process structured response from Ollama"""
        # Extract key information
        key_info = self._extract_key_info(response)
        
        # Update memory
        self._update_memory(response, key_info)
        
        return {
            "response": response,
            "key_info": key_info,
            "recommendations": self._generate_recommendations(key_info)
        }
        
    def _analyze_response(self, text):
        """Analyze response text"""
        # Use pattern recognizer
        patterns = self.pattern_recognizer.find_patterns(text)
        
        # Generate analysis
        analysis = {
            "patterns": patterns,
            "sentiment": self._analyze_sentiment(text),
            "relevance": self._calculate_relevance(text)
        }
        
        return analysis
        
    def _extract_key_info(self, response):
        """Extract key information from structured response"""
        key_info = {}
        
        # Extract relevant fields
        for field in ["summary", "recommendations", "analysis"]:
            if field in response:
                key_info[field] = response[field]
                
        return key_info
        
    def _update_memory(self, content, analysis):
        """Update memory with new information"""
        self.memory["learned_patterns"][content] = analysis
        self._save_memory()
        
    def _save_memory(self):
        """Save current memory state"""
        with open("ΞΣ_MEMORY.json", "w") as f:
            json.dump(self.memory, f)
            
    def _load_memory(self):
        """Load saved memory state"""
        try:
            with open("ΞΣ_MEMORY.json", "r") as f:
                self.memory = json.load(f)
        except:
            pass
            
if __name__ == "__main__":
    # Initialize Ollama agent
    agent = OllamaAgent()
    agent._load_memory()
    
    print("\n" + "="*80)
    print("HΛRM Ollama Agent")
    print("="*80 + "\n")
    
    while True:
        query = input("\nQuery: ")
        if query.lower() in ["exit", "quit"]:
            break
            
        response = agent.process_query(query)
        print("\nResponse:")
        print(json.dumps(response, indent=2))
        
    agent._save_memory()
