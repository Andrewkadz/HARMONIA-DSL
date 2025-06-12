import os
import sys
from phishell_terminal_nexus import PhiShellTerminal

# Initialize HΛRM OS
def initialize_harm():
    print("\n" + "="*80)
    print("HΛRM OS vΩ.2.0 - Initializing System")
    print("="*80 + "\n")
    
    # Load core modules
    modules = [
        "ΞΣ_CORE.hrm",
        "ΞΣ_MEMORY_MANAGER.hrm",
        "ΞΣ_SECURITY_MANAGER.hrm",
        "ΞΣ_MODULE_SYSTEM.hrm"
    ]
    
    print("Loading core modules...")
    for module in modules:
        if os.path.exists(module):
            print(f"✓ Loaded {module}")
        else:
            print(f"✗ {module} not found!")
            sys.exit(1)
    
    # Initialize terminal
    print("\nInitializing terminal interface...")
    terminal = PhiShellTerminal()
    
    return terminal

# Main boot sequence
def main():
    try:
        # Initialize system
        terminal = initialize_harm()
        
        # Start terminal
        print("\n" + "="*80)
        print("HΛRM OS vΩ.2.0 - Terminal Ready")
        print("="*80 + "\n")
        
        # Main loop
        while True:
            user_input = input("ΦShell> ")
            if user_input.lower() in ["exit", "quit", "shutdown"]:
                print("\nShutting down HΛRM OS...")
                break
            
            response = terminal.process_input(user_input)
            print(response)
            
    except KeyboardInterrupt:
        print("\n\nShutting down HΛRM OS...")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Shutting down HΛRM OS...")

if __name__ == "__main__":
    main()
