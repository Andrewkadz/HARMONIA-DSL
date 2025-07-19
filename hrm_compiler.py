# hrm_compiler.py
# Branch: ΞΣ_Engine_Core
# Purpose: Compile and simulate execution of .hrm recursion programs

import os
from pathlib import Path

RECURSION_STACK = {}

SYMBOLS = {
    "Φ": "stabilize",
    "Π": "project",
    "Ψ": "ethics_gate",
    "Θ": "intent",
    "ω": "will_force",
    "ΞΣ": "recursion_node",
    "ΛΨ": "harmonic_pattern",
    "Ω": "closure",
    "ΨΩΣ": "symbolic_high_gamma",
    "Φ₀": "subdelta_field",
    "Ωε": "cosmic_vector"
}


def parse_hrm_line(line):
    if line.strip().startswith("//") or not line.strip():
        return None
    if "ΞΣ" in line and "=" in line:
        node_id = line.split("=")[0].strip()
        expression = line.split("=")[1].strip()
        ops = [s.strip() for s in expression.split("+")]
        return node_id, ops
    return None


def compile_hrm_program(folder):
    program_trace = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".hrm"):
                filepath = Path(root) / file
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f.readlines():
                        result = parse_hrm_line(line)
                        if result:
                            node_id, ops = result
                            program_trace[node_id] = ops
    return program_trace


def simulate(program):
    print("[ΞΣ] Recursive Execution Trace:\n")
    for node, ops in program.items():
        symbolic = [f"{op} → {SYMBOLS.get(op, 'unknown')}" for op in ops]
        print(f"{node}:  {' | '.join(symbolic)}")
    print("\n[Σ] Program convergence evaluation complete.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="Path to .hrmpkg folder")
    args = parser.parse_args()

    hrm_program = compile_hrm_program(args.path)
    simulate(hrm_program)

