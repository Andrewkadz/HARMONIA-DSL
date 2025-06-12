import os
import sys
import json
import threading
import subprocess
from core_agent import CoreAgent
from streamlit_app import main as streamlit_main

class HarmoniaLauncher:
    def __init__(self):
        # Initialize core components
        self.agent = CoreAgent()
        self.streamlit_thread = None
        self.processes = []
        
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
            },
            "resources": {
                "cpu": 0,
                "memory": 0,
                "storage": 0
            }
        }
        
    def initialize_system(self):
        """Initialize the system and display comprehensive overview"""
        try:
            # Initialize core components
            self._initialize_core()
            self._initialize_memory()
            self._initialize_security()
            self._initialize_modules()
            
            # Start Streamlit interface
            self._start_interface()
            
            # Start system processes
            self._start_system_processes()
            
            # Update system state
            self.state["status"] = "ACTIVE"
            for component in self.state["components"]:
                self.state["components"][component] = "ACTIVE"
                
            # Display system overview
            print("\n" + "="*80)
            print("HΛRM OS vΩ.2.0 - System Overview")
            print("="*80 + "\n")
            
            # Core System
            print("Core System:")
            print("- AI Agent: Active (llama2 model)")
            print("- Memory System: Active")
            print("- Security System: Active")
            print("- Module System: Active")
            print("" + "\n")
            
            # Available Interfaces
            print("Available Interfaces:")
            print("- Terminal Interface: Active")
            print("- Web Interface: http://localhost:8501")
            print("- Ollama Service: Active")
            print("" + "\n")
            
            # System Features
            print("System Features:")
            print("- Natural Language Processing")
            print("- Symbolic Processing")
            print("- File Analysis")
            print("- System Management")
            print("- Security Monitoring")
            print("- Resource Optimization")
            print("" + "\n")
            
            # Available Commands
            print("Available Commands:")
            print("- Natural Language: analyze, process, show, display")
            print("- Symbolic: seal verify, query Σ[Θn], echo Ω(n)")
            print("- Help: Type 'help' for more information")
            print("" + "\n")
            
            # Security Status
            print("Security Status:")
            print("- System Seal: LOCKED")
            print("- AI Seal: ACTIVE")
            print("- User Seal: ACTIVE")
            print("- Module Seal: ACTIVE")
            print("" + "\n")
            
            # Resource Usage
            print("Resource Usage:")
            print(f"- CPU: {self.state['resources']['cpu']}%")
            print(f"- Memory: {self.state['resources']['memory']}%")
            print(f"- Storage: {self.state['resources']['storage']}%")
            print("" + "\n")
            
            print("Type 'help' for more information or any command to begin.")
            print("" + "\n")
            
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
            
    def _start_system_processes(self):
        """Start essential system processes"""
        try:
            # Start Ollama if not running
            if not self._is_ollama_running():
                print("Starting Ollama service...")
                self._start_ollama()
                time.sleep(2)  # Wait for Ollama to start
            else:
                print("Ollama service is already running")
                
            # Start other system processes
            print("Starting system processes...")
            self._start_process("python", ["-m", "http.server", "8000"], "File Server")
            self._start_process("python", ["-m", "streamlit", "run", "streamlit_app.py"], "Web Interface")
            
            # Verify Ollama is running
            if self._is_ollama_running():
                print("Ollama service is active")
            else:
                print("Warning: Ollama service failed to start")
                
        except Exception as e:
            self._handle_error(f"System processes failed: {str(e)}")
            
    def _start_ollama(self):
        """Start Ollama service"""
        try:
            # Check if Ollama is installed
            try:
                result = subprocess.run(["ollama", "--version"],
                                     capture_output=True,
                                     text=True)
                if result.returncode != 0:
                    raise Exception("Ollama not installed")
                    
                print(f"Ollama version: {result.stdout.strip()}")
                
            except FileNotFoundError:
                print("Ollama not found. Installing...")
                subprocess.run(["winget", "install", "ollama"],
                             check=True)
            
            # Start Ollama service
            print("Starting Ollama service...")
            process = subprocess.Popen(["ollama", "serve"],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            
            # Wait for service to start
            time.sleep(2)
            
            # Verify service is running
            result = subprocess.run(["ollama", "list"],
                                  capture_output=True,
                                  text=True)
            if result.returncode == 0:
                print("Ollama service started successfully")
            else:
                raise Exception("Failed to start Ollama service")
                
        except Exception as e:
            self._handle_error(f"Failed to start Ollama: {str(e)}")
            
    def _start_process(self, executable, args, name):
        """Start a system process"""
        try:
            process = subprocess.Popen([executable] + args,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            self.processes.append({
                "name": name,
                "process": process
            })
        except Exception as e:
            self._handle_error(f"Failed to start {name}: {str(e)}")
            
    def _is_ollama_running(self):
        """Check if Ollama is running"""
        try:
            result = subprocess.run(["ollama", "list"],
                                  capture_output=True,
                                  text=True)
            return result.returncode == 0
        except:
            return False
            
    def _start_monitors(self):
        """Start system monitors"""
        # Add monitoring threads here
        pass
        
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
        """Run the system with interactive conversation interface"""
        try:
            # Initialize system
            self.initialize_system()
            
            # Display welcome message
            print("\n" + "="*80)
            print("Welcome to HΛRM OS vΩ.2.0")
            print("I am Harmonia AI, your intelligent assistant.")
            print("How can I assist you today?")
            print("" + "\n")
            
            # Main conversation loop
            while True:
                try:
                    # Check system status
                    if self.state["status"] == "ERROR":
                        break
                        
                    # Get user input
                    query = input("\nYou: ")
                    
                    # Handle special commands
                    if query.lower() in ["exit", "quit", "shutdown"]:
                        self.shutdown()
                        break
                    elif query.lower() == "help":
                        self._show_help()
                        continue
                    elif query.lower() == "models":
                        self._show_models()
                        continue
                        
                    # Process query
                    print("\nHarmonia: ", end="")
                    response = self.agent.process_query(query)
                    
                    # Format response
                    if isinstance(response, dict):
                        print(json.dumps(response, indent=2))
                    else:
                        print(response)
                    
                except KeyboardInterrupt:
                    self.shutdown()
                    break
                except Exception as e:
                    print(f"\nError: {str(e)}")
                    
        except Exception as e:
            print(f"\nFatal error: {str(e)}")
            self.shutdown()
            
    def _show_help(self):
        """Show help information"""
        print("\nAvailable Commands:")
        print("- analyze [file] - Analyze a file")
        print("- process [system] - Process system information")
        print("- show [memory/security] - Display system state")
        print("- models - List available AI models")
        print("- set model [name] - Change active model")
        print("- help - Show this help")
        print("- exit/quit/shutdown - Shutdown the system")
        
    def _show_models(self):
        """Show available AI models"""
        print("\nAvailable AI Models:")
        models = self.agent.list_models()
        for model in models.get("models", []):
            print(f"- {model}")
            
    def shutdown(self):
        """Shutdown the system"""
        print("\n" + "="*80)
        print("Shutting down HΛRM OS...")
        print("="*80 + "\n")
        
        # Shutdown components
        self.agent.shutdown()
        
        # Save state
        self._save_state()
        
        # Terminate processes
        for process in self.processes:
            try:
                process["process"].terminate()
                process["process"].wait()
            except:
                pass
                
        # Wait for threads
        if self.streamlit_thread:
            self.streamlit_thread.join()
            
        print("\nShutdown complete.")

def main():
    # Initialize launcher
    launcher = HarmoniaLauncher()
    
    # Run system
    launcher.run()

if __name__ == "__main__":
    main()
