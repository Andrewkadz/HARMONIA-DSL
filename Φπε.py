from phi_pi_e_interpreter import PhiPiEInterpreter
import os

# Initialize interpreter
interpreter = PhiPiEInterpreter()

nexus_file = "NEXUS.hrm"
loader_file = "Φπε_loader.hrm"

def load_nexus():
    if not os.path.exists(nexus_file):
        print("NEXUS.hrm not found. Terminal cannot route input.")
        return []
    with open(nexus_file, "r", encoding="utf-8") as f:
        return f.readlines()

def load_loader():
    if os.path.exists(loader_file):
        with open(loader_file, "r", encoding="utf-8") as f:
            print("ΦShell Loader Activated:")
            print(f.read())
    else:
        print("Φπε_loader.hrm not found. Booting with default context.")

def route_command(command, nexus_lines):
    # First try to execute as Φπε code
    try:
        result = interpreter.execute(command)
        return str(result)
    except Exception as e:
        # If not valid Φπε, try routing through NEXUS
        for line in nexus_lines:
            if "→" in line:
                parts = line.strip().split("→")
                cmd_pattern = parts[0].strip()
                route_target = parts[1].strip()
                if cmd_pattern in command:
                    if cmd_pattern in ["guide", "library", "show symbols", "boot status", "active seal"]:
                        if os.path.exists(route_target):
                            with open(route_target, "r", encoding="utf-8") as module:
                                return module.read()
                        else:
                            return route_target + " not found."
                    else:
                        return "Routed to " + route_target
        if "seal verify" in command:
            return "ΞΣ::SEAL::ΛΞ_ΦΠΨΩ_LOCKED → VERIFIED"
        if "query Σ[Θ" in command:
            return "Σ[Θn] = Cξ → VERIFIED"
        if "echo Ω(n)" in command:
            return "Ω(n) = Harmonic field state coherent"
        return "Command not routed — unrecognized by NEXUS."

# BEGIN: BIOS + Loader Output
print("////////////////////////////////////////////////////////////")
print("//           ΦShell — Harmonic Terminal Boot              //")
print("////////////////////////////////////////////////////////////")
load_loader()
print("////////////////////////////////////////////////////////////")

nexus_lines = load_nexus()
if not nexus_lines:
    exit()

while True:
    cmd = input("ΞΣ_TERM[Φπε] >> ").strip()
    if cmd.lower() == "exit":
        print("Closing ΦShell-Terminal...")
        break
    elif cmd.lower() == "help":
        print("All commands are routed through NEXUS.hrm.")
    else:
        response = route_command(cmd, nexus_lines)
        print(response)
