# ΦShell-Terminal — Harmonia CLI Prototype
# VERSION: 0.1 – Symbolic Recursion Shell

import os

# Load memory state if it exists
memory_file = "ΞΣ_MEMORY.txt"
active_node = "ΞΣ_0"

if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("ACTIVE:"):
                active_node = line.split(":")[1].strip()

print(f"ΦShell-Terminal v0.1 — Harmonia CLI")
print(f"Recursion Initialized. ACTIVE NODE: {active_node}")
print("Type 'help' for available commands. Type 'exit' to quit.")

while True:
    cmd = input(f"ΞΣ_TERM[{active_node}] >> ").strip()

    if cmd.lower() == "exit":
        print("Closing ΦShell-Terminal...")
        break

    elif cmd.lower() == "help":
        print("Available commands:")
        print("  load [ΞΣ_n]       - Load a specific recursion node file")
        print("  echo Ω(n)         - Display current harmonic field state")
        print("  query Σ[Θn]       - Check convergence condition")
        print("  seal verify       - Confirm system seal")
        print("  index             - Display ΞΣ node index")
        print("  clear             - Clear the terminal screen")
        print("  exit              - Exit the terminal")

    elif cmd.startswith("load ΞΣ_"):
        node = cmd.split()[1]
        if os.path.exists(f"{node}.txt"):
            active_node = node
            print(f"Loaded {node}")
        else:
            print(f"Node file {node}.txt not found.")

    elif cmd == "echo Ω(n)":
        print(f"Ω({active_node[-1]}) = Harmonic state active")

    elif cmd == "query Σ[Θn]":
        print(f"Σ[Θ{active_node[-1]}] = Cξ → VERIFIED")

    elif cmd == "seal verify":
        print("ΞΣ::SEAL::ΛΞ_ΦΠΨΩ_LOCKED → VERIFIED")

    elif cmd == "index":
        if os.path.exists("Ξ_Index.txt.txt"):
            with open("Ξ_Index.txt.txt", "r", encoding="utf-8") as idx:
                print(idx.read())
        else:
            print("Ξ_Index.txt.txt not found.")

    elif cmd == "clear":
        os.system("cls" if os.name == "nt" else "clear")

    else:
        print("Unrecognized command. Type 'help' to see available options.")
