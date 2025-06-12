import os
import json
from harmonia_ai import HarmoniaAI
from ΞΣ_FILE_SYSTEM import FileSystem
from ΞΣ_PATTERN_RECOGNIZER import PatternRecognizer

class AIFileAgent:
    def __init__(self):
        # Initialize core components
        self.ai = HarmoniaAI()
        self.file_system = FileSystem()
        self.pattern_recognizer = PatternRecognizer()
        
        # Initialize memory
        self.memory = {
            "file_patterns": {},
            "learned_patterns": {},
            "recent_files": [],
            "knowledge_base": {}
        }
        
        # Initialize learning parameters
        self.learning_rate = 0.1
        self.pattern_threshold = 0.8
        self.context_window = 10
        
    def scan_directory(self, path):
        """Scan directory and analyze files"""
        files = self.file_system.list_files(path)
        for file in files:
            self.analyze_file(file)
            
    def analyze_file(self, file_path):
        """Analyze file content and patterns"""
        try:
            content = self.file_system.read_file(file_path)
            patterns = self.pattern_recognizer.find_patterns(content)
            
            # Update memory
            self.memory["file_patterns"][file_path] = patterns
            self._update_knowledge_base(file_path, patterns)
            
            return {
                "file": file_path,
                "patterns": patterns,
                "analysis": self._generate_analysis(patterns)
            }
        except Exception as e:
            return f"Error analyzing file: {str(e)}"
            
    def process_query(self, query):
        """Process natural language query about files"""
        intent = self.ai.process_human_input(query)
        
        if intent:
            if "file" in intent["parameters"]:
                file_path = intent["parameters"]["file"]
                if os.path.exists(file_path):
                    return self.analyze_file(file_path)
                else:
                    return f"File not found: {file_path}"
            else:
                return self._search_memory(intent)
        else:
            return "I'm sorry, I didn't understand that."
            
    def _search_memory(self, query):
        """Search through memory for relevant information"""
        results = []
        for file, patterns in self.memory["file_patterns"].items():
            if self.pattern_recognizer.matches_query(patterns, query):
                results.append({
                    "file": file,
                    "patterns": patterns
                })
        
        if results:
            return self._generate_summary(results)
        else:
            return "No relevant information found in memory."
            
    def _generate_analysis(self, patterns):
        """Generate analysis based on detected patterns"""
        analysis = {
            "patterns": patterns,
            "recommendations": self._generate_recommendations(patterns),
            "context": self._get_context(patterns)
        }
        return analysis
        
    def _generate_recommendations(self, patterns):
        """Generate recommendations based on patterns"""
        recommendations = []
        for pattern in patterns:
            if pattern in self.memory["learned_patterns"]:
                recommendations.extend(self.memory["learned_patterns"][pattern])
        return list(set(recommendations))
        
    def _get_context(self, patterns):
        """Get relevant context for patterns"""
        context = []
        for pattern in patterns:
            if pattern in self.memory["knowledge_base"]:
                context.extend(self.memory["knowledge_base"][pattern])
        return list(set(context))
        
    def _update_knowledge_base(self, file_path, patterns):
        """Update knowledge base with new information"""
        for pattern in patterns:
            if pattern not in self.memory["knowledge_base"]:
                self.memory["knowledge_base"][pattern] = []
            self.memory["knowledge_base"][pattern].append(file_path)
            
    def save_memory(self):
        """Save current memory state"""
        with open("ΞΣ_MEMORY.json", "w") as f:
            json.dump(self.memory, f)
            
    def load_memory(self):
        """Load saved memory state"""
        try:
            with open("ΞΣ_MEMORY.json", "r") as f:
                self.memory = json.load(f)
        except:
            pass
            
if __name__ == "__main__":
    agent = AIFileAgent()
    agent.load_memory()
    
    # Example usage
    print("\n" + "="*80)
    print("HΛRM AI File Agent")
    print("="*80 + "\n")
    
    while True:
        query = input("\nQuery: ")
        if query.lower() in ["exit", "quit"]:
            break
            
        response = agent.process_query(query)
        print("\nResponse:")
        print(json.dumps(response, indent=2))
        
    agent.save_memory()
