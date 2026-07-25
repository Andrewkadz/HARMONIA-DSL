# hrm_compiler.py
# Compiles and loads Harmonia .hrm grammar files into active symbolic state

import os

HRM_MODULES_PATH = "hrm_modules/"
ΞΣ_STATE = {}

def parse_hrm_line(line):
    """Very basic HRM line parser — expected format: SYMBOL := DEFINITION"""
    if ":=" in line:
        symbol, definition = line.split(":=", 1)
        return symbol.strip(), definition.strip()
    return None, None

def load_hrm_file(filename):
    filepath = os.path.join(HRM_MODULES_PATH, filename)
    if not os.path.exists(filepath):
        return f"Error: {filename} not found in {HRM_MODULES_PATH}"
    
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            symbol, definition = parse_hrm_line(line)
            if symbol:
                ΞΣ_STATE[symbol] = definition
    return f"Loaded {filename} with {len(ΞΣ_STATE)} entries."

def compile_hrm(command):
    """Interpret a symbolic command using loaded HRM grammar"""
    parts = command.strip().split()
    output = []
    
    for token in parts:
        if token in ΞΣ_STATE:
            output.append(f"{token} → {ΞΣ_STATE[token]}")
        else:
            output.append(f"{token} → [undef]")
    
    return "\n".join(output)

def preload_hrm_modules():
    """Automatically load all .hrm modules in hrm_modules/"""
    for fname in os.listdir(HRM_MODULES_PATH):
        if fname.endswith(".hrm"):
            load_hrm_file(fname)

# Optionally preload modules on import
try:
    preload_hrm_modules()
except Exception as e:
    print(f"[hrm_compiler] Failed to preload: {e}")
