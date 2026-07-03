"""
Test suite for HARMONIA / Φπε.

These tests verify the TRUE theorems from RI1:LANGUAGE:Φπε:PROOFS —
the claims that survived honest review — plus basic language guarantees.
Every run of this file is the corpus making contact with reality.
"""

import random
import cmath
from harmonia import HarmoniaVM, parse_complex, HarmoniaError, PHI

random.seed(263 * 97)  # Andrew's numbers, why not

def rand_c(scale=10):
    return complex(random.uniform(-scale, scale), random.uniform(-scale, scale))

passed = failed = 0

def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name}")


print("Theorem 4.2 (Harmonic Stability): |Φ(z,w)| ≤ |z+w|, equality iff z=w")
ok = True
for _ in range(1000):
    z, w = rand_c(), rand_c()
    vm = HarmoniaVM(); vm.field = z
    vm.op_stabilize(w)
    if abs(vm.field) > abs(z + w) + 1e-12:
        ok = False
        break
check("boundedness holds over 1000 random fields", ok)

vm = HarmoniaVM(); z = 3 + 4j; vm.field = z
vm.op_stabilize(z)
check("equality case: Φ(z,z) = z+w exactly", abs(abs(vm.field) - abs(z + z)) < 1e-12)

print("\nTheorem 4.1 (Non-Fusional Property): Φ(z,w) ≠ z+w when z ≠ w")
ok = True
for _ in range(1000):
    z, w = rand_c(), rand_c()
    if z == w:
        continue
    vm = HarmoniaVM(); vm.field = z
    vm.op_stabilize(w)
    if vm.field == z + w:
        ok = False
        break
check("non-fusion holds over 1000 random fields", ok)

print("\nTheorem 4.3 (ε Convergence — with the CORRECTED recurrence)")
# The PDF's recurrence d_{n+1} = d_n²/(1+εd_n) was wrong.
# The true recurrence is d_{n+1} = d_n·(1 − ε/(1+ε·d_n)). Verify BOTH claims:
vm = HarmoniaVM(); vm.field = 1 + 2j
target = 3 + 1j
d_prev = abs(vm.field - target)
monotone = True
recurrence_correct = True
for _ in range(20000):
    d_before = abs(vm.field - target)
    vm.op_micro(target)
    d_after = abs(vm.field - target)
    predicted = d_before * (1 - 0.001 / (1 + 0.001 * d_before))
    if abs(d_after - predicted) > 1e-9:
        recurrence_correct = False
    if d_after > d_before + 1e-15:
        monotone = False
check("distance to target strictly decreases (20,000 steps)", monotone)
check("corrected recurrence predicts every step to 1e-9", recurrence_correct)
check("field converged toward target", abs(vm.field - target) < 0.01 * d_prev + 0.05)

print("\nΠ spiral behavior: phase rotates, iteration does not fixate")
vm = HarmoniaVM(); vm.field = 2 + 3j
phases = []
for _ in range(8):
    vm.op_transcend(1 + 1j, 4)
    phases.append(cmath.phase(vm.field))
check("phase changes across iterations", len(set(round(p, 6) for p in phases)) > 1)

print("\nLanguage guarantees")
prog = "Ε(3+4i) → Φ(1-2i) → Ψ → Ω"
r1 = HarmoniaVM().execute(prog)
r2 = HarmoniaVM().execute(prog)
check("determinism: same program, same result", r1 == r2)

try:
    HarmoniaVM().execute("Ε(1+1i) → Φ(2)")
    check("missing Ω is rejected", False)
except HarmoniaError:
    check("missing Ω is rejected", True)

try:
    HarmoniaVM().execute("Ε(1+1i) → Ω → Φ(2) → Ω")
    check("operation after Ω is rejected", False)
except HarmoniaError:
    check("operation after Ω is rejected", True)

try:
    HarmoniaVM().execute("Ε(1+1i) → Π(0) → Ω")
    check("Π(0) division hazard is rejected", False)
except HarmoniaError:
    check("Π(0) division hazard is rejected", True)

check("complex literals parse: 3+4i", parse_complex("3+4i") == 3 + 4j)
check("complex literals parse: -i", parse_complex("-i") == -1j)
check("complex literals parse: 5", parse_complex("5") == 5 + 0j)

print(f"\n{'='*50}\n{passed} passed, {failed} failed")
raise SystemExit(1 if failed else 0)
