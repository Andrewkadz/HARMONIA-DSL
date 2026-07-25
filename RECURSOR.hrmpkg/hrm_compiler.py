# hrm_compiler.py
# Branch: ΞΣ_Engine_Core
# Purpose: Compile and simulate execution of .hrm recursion programs with UTF-8 safety

import os
import yaml
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

FIELD_CONFIG = {}

def load_field_config(folder):
    global FIELD_CONFIG
    config_path = Path(folder) / "field_config.yml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            FIELD_CONFIG = yaml.safe_load(f)
            print("[ΞΣ] Field configuration loaded.")
    else:
        print("[!] No field_config.yml found.")

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
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line in f.readlines():
                            result = parse_hrm_line(line)
                            if result:
                                node_id, ops = result
                                program_trace[node_id] = ops
                except UnicodeDecodeError as e:
                    print(f"[✗] Unicode decode error in file {filepath}: {e}")
    return program_trace

def simulate(program):
    print("[ΞΣ] Recursive Execution Trace:\n")
    trace_lines = []
    for node, ops in program.items():
        symbolic = [f"{op} → {SYMBOLS.get(op, 'unknown')}" for op in ops]
        trace_output = f"{node}:  {' | '.join(symbolic)}"
        print(trace_output)
        trace_lines.append(trace_output)

    trace_log = FIELD_CONFIG.get("trace_output", "ΞΣ_trace.hrmlog")
    with open(trace_log, 'w', encoding='utf-8') as log:
        log.write("// ΞΣ TRACE LOG\n")
        for line in trace_lines:
            log.write(line + "\n")
    print(f"\n[Σ] Trace written to {trace_log}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="Path to .hrmpkg folder")
    args = parser.parse_args()

    load_field_config(args.path)
    hrm_program = compile_hrm_program(args.path)
    simulate(hrm_program)
