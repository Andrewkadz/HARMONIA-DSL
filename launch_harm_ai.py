import os
import sys
import json
import threading
from core_agent import CoreAgent
from streamlit_app import main as streamlit_main

class HarmLauncher:
    def __init__(self):
        # Initialize core components
        self.agent = CoreAgent()
        self.streamlit_thread = None
        
        # Initialize system state
        self.state = {
            "phase": "ΞΣ_PHASE_3.0",
            "status": "INITIALIZING",
            "identity": "ΞΣ::SEAL::ΛΞ_ΦΠΨΩ_LOCKED",
            "components": {
                "core": "INITIALIZING",
                "memory": "INITIALIZING",
                "security": "INITIALIZING",
                "modules": "INITIALIZING",
                "interface": "INITIALIZING"
            }
        }
        
    def initialize_system(self):
        """Initialize the system"""
        try:
            # Initialize core components
            self._initialize_core()
            self._initialize_memory()
            self._initialize_security()
            self._initialize_modules()
            
            # Start Streamlit interface
            self._start_interface()
            
            # Update system state
            self.state["status"] = "ACTIVE"
            for component in self.state["components"]:
                self.state["components"][component] = "ACTIVE"
                
            print("\n" + "="*80)
            print("HΛRM OS vΩ.2.0 - Initialization Complete")
            print("="*80 + "\n")
            
        except Exception as e:
            self._handle_error(f"System initialization failed: {str(e)}")
            
    def _initialize_core(self):
        """Initialize core agent"""
        try:
            self.agent.initialize()
            self.state["components"]["core"] = "INITIALIZED"
        except Exception as e:
            self._handle_error(f"Core initialization failed: {str(e)}")
            
    def _initialize_memory(self):
        """Initialize memory system"""
        try:
            self.agent.memory.initialize()
            self.state["components"]["memory"] = "INITIALIZED"
        except Exception as e:
            self._handle_error(f"Memory initialization failed: {str(e)}")
            
    def _initialize_security(self):
        """Initialize security system"""
        try:
            self.agent.security.initialize()
            self.state["components"]["security"] = "INITIALIZED"
        except Exception as e:
            self._handle_error(f"Security initialization failed: {str(e)}")
            
    def _initialize_modules(self):
        """Initialize module system"""
        try:
            self.agent.modules.initialize()
            self.state["components"]["modules"] = "INITIALIZED"
        except Exception as e:
            self._handle_error(f"Module initialization failed: {str(e)}")
            
    def _start_interface(self):
        """Start Streamlit interface"""
        try:
            self.streamlit_thread = threading.Thread(
                target=streamlit_main,
                daemon=True
            )
            self.streamlit_thread.start()
            self.state["components"]["interface"] = "INITIALIZED"
        except Exception as e:
            self._handle_error(f"Interface initialization failed: {str(e)}")
            
    def _handle_error(self, error):
        """Handle system errors"""
        print(f"\nError: {error}")
        self.state["status"] = "ERROR"
        self._save_state()
        
    def _save_state(self):
        """Save system state"""
        with open("ΞΣ_STATE.json", "w") as f:
            json.dump(self.state, f)
            
    def run(self):
        """Run the system"""
        try:
            # Initialize system
            self.initialize_system()
            
            # Main loop
            while True:
                try:
                    # Check system status
                    if self.state["status"] == "ERROR":
                        break
                        
                    # Process user input
                    query = input("\nQuery: ")
                    if query.lower() in ["exit", "quit", "shutdown"]:
                        self.shutdown()
                        break
                        
                    # Process query
                    response = self.agent.process_query(query)
                    print("\nResponse:")
                    print(json.dumps(response, indent=2))
                    
                except KeyboardInterrupt:
                    self.shutdown()
                    break
                except Exception as e:
                    print(f"\nError: {str(e)}")
                    
        except Exception as e:
            print(f"\nFatal error: {str(e)}")
            self.shutdown()
            
    def shutdown(self):
        """Shutdown the system"""
        print("\n" + "="*80)
        print("Shutting down HΛRM OS...")
        print("="*80 + "\n")
        
        # Shutdown components
        self.agent.shutdown()
        
        # Save state
        self._save_state()
        
        # Wait for threads
        if self.streamlit_thread:
            self.streamlit_thread.join()
            
        print("\nShutdown complete.")

def main():
    # Initialize launcher
    launcher = HarmLauncher()
    
    # Run system
    launcher.run()

if __name__ == "__main__":
    main()
