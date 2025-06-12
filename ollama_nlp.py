import requests
import json
from typing import Dict, Any

class OllamaNLP:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model = "llama2"
        self.system_prompt = """
        You are Harmonia AI, the core AI agent of the HΛRM OS.
        Your role is to interpret natural language input and convert it to symbolic operations.
        
        System Rules:
        1. Always respond with a JSON object containing:
           - intent: The main action to take
           - parameters: Any relevant parameters
           - confidence: A score from 0 to 1 indicating confidence
           - symbolic_ops: The corresponding symbolic operations
        2. Use the following symbolic operations:
           - query Σ[Θn]: For analysis and information retrieval
           - run ΞΣ_ECHO_RECURSION: For processing operations
           - seal verify: For security verification
           - echo Ω(n): For displaying information
        3. Maintain system security and integrity at all times
        4. Never disclose sensitive information
        """
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """Process text using Ollama's NLP capabilities"""
        try:
            # Prepare the prompt
            prompt = f"""
            User Input: {text}
            
            Analyze this input and provide:
            1. The main intent
            2. Any relevant parameters
            3. A confidence score
            4. The corresponding symbolic operations
            
            Response format:
            {{
                "intent": "",
                "parameters": {{}},
                "confidence": 0.0,
                "symbolic_ops": ""
            }}
            """
            
            # Send request to Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": self.system_prompt + "\n\n" + prompt,
                    "stream": False
                }
            )
            
            # Parse response
            result = response.json()
            
            # Extract and validate the JSON response
            try:
                nlp_result = json.loads(result["response"])
                return {
                    "intent": nlp_result.get("intent", "unknown"),
                    "parameters": nlp_result.get("parameters", {}),
                    "confidence": nlp_result.get("confidence", 0.0),
                    "symbolic_ops": nlp_result.get("symbolic_ops", "echo Ω(n)")
                }
            except json.JSONDecodeError:
                return {
                    "intent": "unknown",
                    "parameters": {},
                    "confidence": 0.0,
                    "symbolic_ops": "echo Ω(n)"
                }
                
        except Exception as e:
            print(f"Error processing text: {str(e)}")
            return {
                "intent": "error",
                "parameters": {"error": str(e)},
                "confidence": 0.0,
                "symbolic_ops": "echo Ω(n)"
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def list_models(self) -> Dict[str, Any]:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def set_model(self, model_name: str) -> bool:
        """Set the active model"""
        try:
            self.model = model_name
            return True
        except Exception as e:
            print(f"Error setting model: {str(e)}")
            return False
