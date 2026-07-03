"""Honest test harness for the Φπε interpreter from HARMONIA-DSL."""
import sys, traceback

sys.path.insert(0, ".")
from phi_pi_e_interpreter import PhiPiEInterpreter

programs = [
    ("single symbol phi", "Φ"),
    ("single symbol epsilon", "Ε"),
    ("flow expression", "Ε→Φ"),
    ("numeric field", "Φ:1.5"),
    ("loop expression", "[Φ+Ψ]"),
    ("nested expression", "Ξ(Φ:2)"),
    ("full sequence", "Θ→Ε→Φ→Ω"),
]

passed, failed = 0, 0
for name, prog in programs:
    print("=" * 60)
    print(f"TEST: {name}   PROGRAM: {prog}")
    try:
        interp = PhiPiEInterpreter()
        result = interp.execute(prog)
        print(f"RESULT: {result!r}")
        passed += 1
    except Exception as e:
        print(f"CRASHED: {type(e).__name__}: {e}")
        traceback.print_exc(limit=2)
        failed += 1

print("=" * 60)
print(f"SUMMARY: {passed} ran without crashing, {failed} crashed, out of {len(programs)}")
