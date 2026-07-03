"""
HARMONIA / Φπε — a working interpreter.

Language: Andrew Josef Kadziolka (Φπε formalism, 2021–2026)
Implementation: rebuilt 2026-07-03 so the language actually executes.

Design principle: every glyph's semantics comes from Andrew's own operator
definitions (RI1:LANGUAGE:Φπε:PROOFS) — but only the parts that are
mathematically true. The state of a program is a complex number: the field.

Glyphs:
    Ε(w)      ignite      — set the field to w
    Φ(w)      stabilize   — z ← φ(z+w)/(φ+|z−w|)          [bounded, non-fusional]
    ε(w)      micro-step  — z ← z + ε(w−z)/(1+ε|w−z|)     [converges toward w]
    Π(w, n)   transcend   — z ← π(z + w·e^{iπ/n})/(1+|z|/|w|)  [spiral phase]
    Λ(w)      illuminate  — z ← Λ·2Re(z̄w)/(Λ+|z|²+|w|²)   [real coupling]
    Δ(w)      fuse        — z ← Δ·zw/(Δ+Λ|z−w|)           [irreversible product]
    Ψ         pulse       — z ← z·e^{iπ/2}                 [quarter-turn]
    Ω         close       — emit the field and halt

Syntax: one operation per line, or chained with →. Comments start with #.
Complex literals: 3+4i, 1-2i, 2i, 5, -i
"""

import cmath
import math
import re
import sys

# Andrew's constants (kept exactly as defined in the Φπε corpus)
PHI = 89 / 55          # Fibonacci approximation to the golden ratio
PI_C = 22 / 7          # Archimedean approximation to pi
EPS = 0.001            # incremental insight threshold
LAM = 137 / 3          # structural illumination constant
DEL = LAM ** 2         # fusion transformation constant


class HarmoniaError(Exception):
    pass


def parse_complex(s: str) -> complex:
    """Parse a Φπε complex literal like 3+4i, -2i, 5, i."""
    s = s.strip().replace(" ", "").replace("i", "j")
    s = re.sub(r"(?<![0-9.])j", "1j", s)  # i -> 1j, +i -> +1j, -i -> -1j
    try:
        return complex(s)
    except ValueError:
        raise HarmoniaError(f"cannot parse complex literal: {s!r}")


class HarmoniaVM:
    def __init__(self):
        self.field: complex = 0j
        self.closed = False
        self.trace: list[tuple[str, complex]] = []

    # ── operator semantics (one method per glyph) ──────────────────────

    def op_ignite(self, w: complex) -> None:
        self.field = w

    def op_stabilize(self, w: complex) -> None:
        z = self.field
        self.field = PHI * (z + w) / (PHI + abs(z - w))

    def op_micro(self, w: complex) -> None:
        z = self.field
        self.field = z + EPS * (w - z) / (1 + EPS * abs(w - z))

    def op_transcend(self, w: complex, n: int = 4) -> None:
        if w == 0:
            raise HarmoniaError("Π requires w ≠ 0")
        if n < 1:
            raise HarmoniaError("Π requires n ≥ 1")
        z = self.field
        spiral = cmath.exp(1j * PI_C / n)
        self.field = PI_C * (z + w * spiral) / (1 + abs(z) / abs(w))

    def op_illuminate(self, w: complex) -> None:
        z = self.field
        coupling = 2 * (z.conjugate() * w).real
        self.field = complex(LAM * coupling / (LAM + abs(z) ** 2 + abs(w) ** 2))

    def op_fuse(self, w: complex) -> None:
        z = self.field
        self.field = DEL * (z * w) / (DEL + LAM * abs(z - w))

    def op_pulse(self) -> None:
        self.field = self.field * cmath.exp(1j * PI_C / 2)

    def op_close(self) -> None:
        self.closed = True

    # ── parsing and execution ──────────────────────────────────────────

    GLYPHS = {
        "Ε": ("ignite", 1), "E": ("ignite", 1),
        "Φ": ("stabilize", 1),
        "ε": ("micro", 1),
        "Π": ("transcend", (1, 2)),
        "Λ": ("illuminate", 1),
        "Δ": ("fuse", 1),
        "Ψ": ("pulse", 0),
        "Ω": ("close", 0),
    }

    def execute(self, source: str) -> complex:
        # strip comments, split lines, then split chains on →
        steps = []
        for line in source.splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            steps.extend(s.strip() for s in line.split("→") if s.strip())

        if not steps:
            raise HarmoniaError("empty program")

        for step in steps:
            if self.closed:
                raise HarmoniaError(f"operation after Ω: {step!r}")
            self._execute_step(step)

        if not self.closed:
            raise HarmoniaError("program must end with Ω (closure)")
        return self.field

    def _execute_step(self, step: str) -> None:
        m = re.fullmatch(r"(\S)\s*(?:\(([^)]*)\))?", step)
        if not m:
            raise HarmoniaError(f"cannot parse step: {step!r}")
        glyph, argstr = m.group(1), m.group(2)

        if glyph not in self.GLYPHS:
            raise HarmoniaError(f"unknown glyph: {glyph!r}")
        name, arity = self.GLYPHS[glyph]

        args = []
        if argstr:
            parts = [p for p in argstr.split(",") if p.strip()]
            if parts:
                args.append(parse_complex(parts[0]))
            if len(parts) > 1:
                args.append(int(parts[1]))

        if isinstance(arity, tuple):
            ok = arity[0] <= len(args) <= arity[1]
        else:
            ok = len(args) == arity
        if not ok:
            raise HarmoniaError(f"{glyph} given {len(args)} argument(s), expects {arity}")

        getattr(self, f"op_{name}")(*args)
        self.trace.append((step, self.field))

    def report(self) -> str:
        lines = ["  step             field value"]
        for step, value in self.trace:
            lines.append(f"  {step:<16} {value.real:+.6f} {value.imag:+.6f}i   |field|={abs(value):.6f}")
        return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print("usage: python harmonia.py program.hrm")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        source = f.read()
    vm = HarmoniaVM()
    result = vm.execute(source)
    print("HARMONIA Φπε — execution trace")
    print(vm.report())
    print(f"\nΩ closure: field = {result.real:+.6f} {result.imag:+.6f}i, "
          f"magnitude = {abs(result):.6f}, phase = {math.degrees(cmath.phase(result)):.2f}°")


if __name__ == "__main__":
    main()
