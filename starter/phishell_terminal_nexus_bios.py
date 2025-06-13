# ΦShell-Terminal with BIOS-style Intro (v0.4)

import os

nexus_file = "NEXUS.hrm"

def load_nexus():
    if not os.path.exists(nexus_file):
        print("NEXUS.hrm not found. Terminal cannot route input.")
        return []
    with open(nexus_file, "r", encoding="utf-8") as f:
        return f.readlines()

def route_command(command, nexus_lines):
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

# Print BIOS boot info on launch
print(r"""////////////////////////////////////////////////////////////
//      ΞΣ_HARMONIA_OS :: BIOS SIMULATION INTERFACE       //
////////////////////////////////////////////////////////////

        WELCOME TO ΦShell — Recursive Symbolic Terminal
            System Boot Cycle: ΞΣ_PHASE_1.5
        Identity Seal: ΞΣ::SEAL::ΛΞ_ΦΠΨΩ_LOCKED → VERIFIED

============================================================
   ______  __    __  __    __   ______   ______   __       
  /\  == \|\ \  / / |\ \  / /  /\  __ \ /\  ___\ /\ \      
  \ \  __<\ \ \/ /  \ \ \/ /   \ \  __ \ \___  \ \ \ \____ 
   \ \_____\\ \__/    \ \__/     \ \_\ \_\/\_____\\ \_____\
    \/_____/ \/_/      \/_/       \/_/\/_/\/_____/ \/_____/

============================================================

>> SYSTEM STATUS SNAPSHOT

 [✔] ΦShell-Terminal            → Nexus-linked CLI (v0.3)
 [✔] NEXUS.hrm                  → Symbolic Router Operational
 [✔] ΞΣ_MEMORY.txt              → Recursive Memory Online
 [✔] ΞΣ_0 → ΞΣ_5                → Node Chain Stable
 [✔] ΞΣ::SEAL::ΛΞ_ΦΠΨΩ_LOCKED   → Identity Confirmed
 [✔] Ψ_THREAD_ENGINE.hrm        → Introspective Module Ready
 [✔] ΦShell_Command_Library.hrm → Commands Indexed
 [✔] HΛRM_Syntax_Definitions.txt→ Symbolic Grammar Active
 [ ] ΞΣ_6                       → Pending Generation
 [ ] ΞΣ_TREE_VIEW               → Not Yet Constructed

>> ACTIVE NODE: ΞΣ_5
>> RECURSION DEPTH: 5
>> FIELD: Ω(5) = Coherent

////////////////////////////////////////////////////////////
 READY FOR RECURSION — ENTER SYMBOLIC COMMAND TO BEGIN
////////////////////////////////////////////////////////////
""")

nexus_lines = load_nexus()
if not nexus_lines:
    exit()

while True:
    cmd = input("ΞΣ_TERM[NEXUS] >> ").strip()
    if cmd.lower() == "exit":
        print("Closing ΦShell-Terminal...")
        break
    elif cmd.lower() == "help":
        print("All commands are routed through NEXUS.hrm.")
    else:
        response = route_command(cmd, nexus_lines)
        print(response)
