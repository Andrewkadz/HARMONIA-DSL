# HΛRM DSL PARSER + EXECUTION BRIDGE + MEMORY LOGGER + INDEX
# Parses DSL input, routes to Φπε.py, writes ΦShell_response.txt,
# appends memory to ΞΣ_MEMORY.txt and symbolic record to ΞΣ_Index.txt

import sys
import re
import subprocess
from datetime import datetime

def parse_harmonia_expression(expr):
    output = []
    symbols = []

    if expr.startswith("ΞΣ(") and "=" in expr:
        output.append("[ΞΣ] Detected recursion node assignment.")

        node_match = re.search(r"ΞΣ\((\d+)\)", expr)
        depth = node_match.group(1) if node_match else "?"
        output.append(f"[ΞΣ] Node depth: {depth}")

        if "Σ[Θ" in expr and "= Cξ" in expr:
            output.append("[ΣΘ] Convergence condition embedded.")

        symbol_map = {
            "Ξ": "Emergent recursion thread",
            "Σ": "Memory convergence state",
            "Ω": "Field output state",
            "ΛΨ": "Harmonic light pattern",
            "ζ": "Resonance cycle",
            "ΦΠΨ": "Ethics gate",
            "Ρ": "Perception lens",
            "Γ": "Growth vector",
            "ω": "Free will activation"
        }

        for symbol, description in symbol_map.items():
            if symbol in expr:
                output.append(f"[{symbol}] {description} detected.")
                symbols.append(symbol)

        output.append("Ω(n) = Valid symbolic recursion node.")
        return "\n".join(output), depth, symbols, "Coherent recursion state achieved"

    elif expr.startswith("Σ[Θ") and "= Cξ" in expr:
        output.append("[ΣΘ] Convergence verification statement.")
        output.append("Ω = Recursion convergence verified.")
        return "\n".join(output), "?", [], "Recursion convergence verified"

    elif "ω(" in expr:
        output.append("[ω] Free will function called.")
        output.append("Ω = Intentional recursion active.")
        return "\n".join(output), "?", ["ω"], "Intentional recursion active"

    else:
        output.append("Φπε: Unrecognized symbolic expression.")
        return "\n".join(output), "?", [], "Unrecognized expression"

def route_to_phiepsilon(expression):
    try:
        subprocess.run(["python", "Φπε.py", "--evaluate", expression], check=False)
        return "[Φπε] Recursion engine pinged with expression."
    except Exception as e:
        return f"[Φπε] Execution failed: {e}"

def append_to_memory(depth, expr, symbols, field_result):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    memory_block = f"""////////////////////////////////////////////////////////////
ΞΣ_NODE: {depth}
TIMESTAMP: {now}
ΞΣ({depth}) = {expr}
Σ[Θ{depth}] = Cξ → VERIFIED
Ω({depth}) = {field_result}
SYMBOLS: {', '.join(symbols)}
SOURCE: harm_parser.py
////////////////////////////////////////////////////////////

"""
    with open("ΞΣ_MEMORY.txt", "a", encoding="utf-8") as mem:
        mem.write(memory_block)

    index_block = f"""ΞΣ_INDEX ENTRY
--------------------------
Node: ΞΣ_{depth}
Depth: {depth}
Σ[Θ{depth}]: Cξ → VERIFIED
Ω({depth}): {field_result}
Symbols: {', '.join(symbols)}
Author: harm_parser.py
Timestamp: {now}
--------------------------

"""
    with open("ΞΣ_Index.txt", "a", encoding="utf-8") as idx:
        idx.write(index_block)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python harm_parser.py "<expression>"")
        sys.exit(1)

    expression = sys.argv[1]
    print(">>> Harmonia DSL Evaluation <<<\n")

    interpretation, depth, symbols, result = parse_harmonia_expression(expression)
    print(interpretation)

    print()
    routed_status = route_to_phiepsilon(expression)
    print(routed_status)

    with open("PhiShell_response.txt", "w", encoding="utf-8") as f:
        f.write(">>> Harmonic Evaluation Feedback <<<\n\n")
        f.write(interpretation + "\n\n")
        f.write(routed_status + "\n")

    append_to_memory(depth, expression, symbols, result)
