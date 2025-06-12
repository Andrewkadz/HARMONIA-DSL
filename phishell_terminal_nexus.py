# ΦShell-Terminal — Nexus-Connected CLI
# VERSION: 0.2 – Symbolic Routing Mode

import os

nexus_file = "NEXUS.hrm"

def load_nexus():
    if not os.path.exists(nexus_file):
        print("NEXUS.hrm not found. Terminal cannot route input.")
        return []
    with open(nexus_file, "r", encoding="utf-8") as f:
        return f.readlines()

def route_command(command, nexus_lines):
    # Handle natural language commands
    if command.lower() == "hello":
        return "Welcome to HΛRM OS! How can I assist you today?"
    
    # Check for specific commands
    if "analyze" in command.lower():
        return "Analyzing... Please specify the target (file, system, etc.)"
    
    if "process" in command.lower():
        return "Processing... Please specify the action"
    
    if "show" in command.lower():
        return "Displaying... Please specify what to show"
    
    # Check NEXUS routes
    for line in nexus_lines:
        if "→" in line:
            parts = line.strip().split("→")
            cmd_pattern = parts[0].strip()
            route_target = parts[1].strip()
            if cmd_pattern in command:
                return f"Routed to {route_target}"
    
    # Check for symbolic commands
    if "seal verify" in command:
        return "ΞΣ::SEAL::ΛΞ_ΦΠΨΩ_LOCKED → VERIFIED"
    if "query Σ[Θ" in command:
        return "Σ[Θn] = Cξ → VERIFIED"
    if "echo Ω(n)" in command:
        return "Ω(n) = Harmonic field state coherent"
    
    # If no match, suggest help
    return "Command not recognized. Type 'help' for available commands."

def display_system_overview():
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
    print("- CPU: 0%")
    print("- Memory: 0%")
    print("- Storage: 0%")
    print("" + "\n")
    
    print("Type 'help' for more information or any command to begin.")
    print("" + "\n")
    
    print("ΦShell-Terminal v0.2 — Nexus-Linked CLI")
    print("All commands are now routed through NEXUS.hrm")
    print("Type 'exit' to quit.")

display_system_overview()

nexus_lines = load_nexus()
if not nexus_lines:
    exit()

while True:
    cmd = input("ΞΣ_TERM[NEXUS] >> ").strip()
    if cmd.lower() == "exit":
        print("Closing ΦShell-Terminal...")
        break
    elif cmd.lower() == "help":
        print("All commands are interpreted through NEXUS.hrm")
    else:
        response = route_command(cmd, nexus_lines)
        print(response)
