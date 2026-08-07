"""HARMONIA-DSL Interpreter

This interpreter implements the core stabilization formula derived from
the Grand Harmonic Equation (R):

    R = [ lim ( ΨΩ → ∞ ) ] * { ( Ξ / Λc ) * [ ( 1 - ∂Ω / ∂Ψ ) ] }  
          +  Σ [ Θn ]  
          +  { F(P) * V }  
          +  [ ΔΩ(T) / S ]  
          +  { Ψ± * K }  
          +  ({ Φ * β })  
          +  [ Cξ / Eψ ]  
          +  { Γ ( ΨΩ, F(P), ΔΩ ) }

The current implementation (v1.0) focuses on the core stabilization:
    Σ = (Ψ + Φ) * (1 - ε)

For the complete theoretical foundations, see /theory/RI1_GRANDHARMONICEQUATION.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Union, Optional, Set
import cmath
import math
import re

PHI_RATIONAL_LOCAL = 89 / 55   # Fibonacci convergent, used by Ξ
import numpy as np
from collections import defaultdict, deque
from enum import Enum
import uuid

@dataclass
class FieldTension:
    """Represents the tension between recursive fields"""
    strength: float = 0.0
    phase: float = 0.0
    charge: float = 0.0
    
    def __add__(self, other: 'FieldTension') -> 'FieldTension':
        return FieldTension(
            strength=self.strength + other.strength,
            phase=(self.phase + other.phase) / 2,
            charge=self.charge + other.charge
        )
    
    def __sub__(self, other: 'FieldTension') -> 'FieldTension':
        return FieldTension(
            strength=self.strength - other.strength,
            phase=(self.phase - other.phase) / 2,
            charge=self.charge - other.charge
        )

@dataclass
class RecursiveState:
    """Represents a recursive state in the field"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    depth: int = 0
    parent: Optional[str] = None
    children: Set[str] = field(default_factory=set)
    tension: FieldTension = field(default_factory=FieldTension)
    phase: float = 0.0
    charge: float = 0.0
    
    # ΦπεNode fields (for Phi-Coder-AI integration)
    psi_signal: float = 0.0      # ψ: Recursive animation signal
    phi_state: float = 0.0        # φ: Harmonic equilibrium state
    epsilon_drift: float = 0.0    # ε: Incremental drift/error
    stabilized_value: float = 0.0 # Result of stabilization
    
    def add_child(self, child_id: str) -> None:
        self.children.add(child_id)
    
    def remove_child(self, child_id: str) -> None:
        self.children.discard(child_id)

@dataclass
class FieldContext:
    """Context for field evaluation"""
    state: RecursiveState
    tension: FieldTension
    phase: float
    charge: float
    depth: int
    
    def __init__(self, state: Optional[RecursiveState] = None,
                 zfield: Optional[Dict[str, complex]] = None):
        if state is None:
            state = RecursiveState()
        self.state = state
        self.tension = state.tension
        self.phase = state.phase
        self.charge = state.charge
        self.depth = state.depth
        # Shadow register layer (BRIDGE_DESIGN Decision 1, Step 1).
        # Complex registers for the Φπε math core. STRICTLY isolated
        # from the real scalars: nothing in this dict may read or write
        # psi_signal / phi_state / epsilon_drift / stabilized_value.
        # Populated by @name syntax (Step 2) and math-core register ops.
        self.zfield: Dict[str, complex] = zfield if zfield is not None else {}
        # Dedicated Λ-reduction observable (BRIDGE_DESIGN resolved item 3).
        # Real-valued; the ONLY landing site for ℂ→ℝ reduction. Never
        # aliased to pinned scalars.
        self.lambda_obs: float = 0.0
        # ===== LOGIC_NODES_DESIGN: scalar field + structural slots =====
        # #name attributes at root. Never alias pinned ΦπεNode state.
        self.scalars: Dict[str, float] = {}
        # Σ superposition: name -> ordered list of complex members
        self.superpositions: Dict[str, List[complex]] = {}
        # Ξ composition: name -> membership list
        self.composites: Dict[str, List[str]] = {}
        # Γ lineage: name -> list of prior values (generation = len)
        self.lineage: Dict[str, List[complex]] = {}
        # ζ recurrence: name -> bounded history of register signatures
        self.history: Dict[str, List[complex]] = {}
        self.history_maxlen: int = 64

    # ---- scalar field ----
    def set_scalar(self, name: str, value: float) -> None:
        self.scalars[name] = float(value)

    def get_scalar(self, name: str) -> float:
        return self.scalars.get(name, 0.0)

    def record_history(self, name: str, value: complex) -> None:
        h = self.history.setdefault(name, [])
        h.append(value)
        if len(h) > self.history_maxlen:
            del h[0]

    def write_register(self, name: str, value: complex) -> None:
        """Write a complex value to a named shadow register.

        Ints/floats are coerced to complex (imag=0). Per BRIDGE_DESIGN,
        registers are the ONLY residence of ℂ values; this method never
        touches real scalar state.
        """
        self.zfield[name] = complex(value)

    def read_register(self, name: str) -> complex:
        """Read a named shadow register; unset registers read as 0j."""
        return self.zfield.get(name, 0j)

    def fork(self) -> 'FieldContext':
        """Create a new context with increased depth.

        The shadow register layer is SHARED with the fork (same dict):
        registers are execution-global, like the persistent context in
        the time model. Fork/discard cycles by modulators must not
        create divergent register copies.
        """
        new_state = RecursiveState(
            parent=self.state.id,
            depth=self.depth + 1,
            tension=self.tension,
            phase=self.phase,
            charge=self.charge
        )
        self.state.add_child(new_state.id)
        child = FieldContext(new_state, zfield=self.zfield)
        child.lambda_obs = self.lambda_obs  # carried like phase/charge
        # structural layers are execution-global, like zfield
        child.scalars = self.scalars
        child.superpositions = self.superpositions
        child.composites = self.composites
        child.lineage = self.lineage
        child.history = self.history
        return child

    def merge(self, other: 'FieldContext') -> None:
        """Merge another context into this one"""
        self.tension = self.tension + other.tension
        self.phase = (self.phase + other.phase) / 2
        self.charge = self.charge + other.charge

class PhiPiEInterpreterFixed:
    def __init__(self):
        self.fields: Dict[str, Any] = {}
        self.symbols = {
            'Φ': self.stabilize,         # Harmonic Equilibrium
            'Π': self.transcend,         # Transcendent Continuity
            'Ε': self.ignite,           # Ignition / Initiation
            'ε': self.micro_ignite,     # Micro-Ignition
            'Δ': self.fuse,             # Fusion / Transformation
            'δ': self.micro_transform,  # Micro-Transformation
            'Ψ': self.pulse,            # Oscillation / Recursive Pulse
            'Λ': self.illuminate,       # Structural Illumination
            'λ': self.entangle,         # Entanglement
            'Γ': self.grow,             # Recursive Growth
            'Ω': self.close,            # Closure
            'ω': self.will_force,       # Will-Force
            'Σ': self.coexist,          # Coexistence
            'Ξ': self.emerge,           # Emergent System
            'ζ': self.recurrence,       # Recurrence Pattern
            'Τ': self.synchronize,      # Synchronization
            'Ρ': self.perceive,         # Perception Modulation
            'Θ': self.intend,           # Intention
            'η': self.index,            # Index / Parameter
            'χ': self.measure,          # Measurement
            'n': self.index,            # Index (alternative)
            # Grok's operators (added Dec 31, 2025)
            'Κ': self.probe,            # Query Probe (Kappa)
            'Υ': self.consensus_merge,  # Consensus Merge (Upsilon)
            'Β': self.reflection_echo   # Reflection Echo (Beta)
        }
        
        self.operators = {
            '→': self.flow,           # Flow Vector
            '+': self.simultaneity,   # Simultaneity
            ':': self.interact,       # Interaction
            '/': self.disrupt,        # Disruption
            '|': self.orthogonal,     # Orthogonality
            '[]': self.loop,          # Loop
            '=': self.stabilize       # Stabilization
        }

        # ===== OPERATOR CATEGORIES (feat/operator-categories) =====
        # Categorical execution model aligned with the Φπε operator
        # architecture (Φ→π→ε→Λ→Δ→Ω→Ψ→Ξ→Γ→Σ→ζ→λ→ω→Τ→Ρ→δ→Θ).
        # Uniform argument rule per category:
        #   SETTERS    consume adjacent numeric literals into semantic
        #              state (psi_signal / phi_state / epsilon_drift).
        #   REDUCERS   take no literal arguments; read semantic state and
        #              return a scalar observation/result.
        #   MODULATORS operate on context mechanics (phase/charge/depth);
        #              they never consume literals and return no scalar.
        # This replaces per-symbol special-casing in the dispatcher and is
        # the seed of a future AST. Full semantics for modulators are
        # intentionally NOT implemented yet — see SYMBOL_COVERAGE.md.
        # Tier-2 structural operators (LOGIC_NODES_DESIGN). Dispatched
        # only when followed by register operands, so the tier-1
        # semantics of reused glyphs (Σ as reducer, Γ/ζ/Τ as
        # modulators) are untouched — operand-kind dispatch, exactly
        # as BRIDGE_DESIGN Decision 2 prescribes.
        self.structural = {
            'Σ': self._sigma_superpose,
            'Σ!': self._sigma_collapse,
            'ζ': self._zeta_recurrence,
            'Ξ': self._xi_compose,
            'Γ': self._gamma_evolve,
            'Τ': self._tau_phaselock,
        }

        self.categories = {
            'setter': {'Φ', 'Ψ', 'ε'},
            'reducer': {'Σ', 'Κ', 'Υ', 'Β'},
            # Γ (growth) and ζ (recurrence) are candidate reducers per the
            # Φπε architecture, but currently only touch phase/charge, so
            # they stay modulators until given real read-state semantics.
            'modulator': {'Π', 'Ε', 'Δ', 'δ', 'Λ', 'λ', 'Γ', 'Ω', 'ω',
                          'Ξ', 'ζ', 'Τ', 'Ρ', 'Θ', 'η', 'χ', 'n'},
        }

    # ===== TIER 2: structural operators (LOGIC_NODES_DESIGN) =====
    # Computational realizations chosen to fulfil the roles the proofs
    # assign — NOT derivations from the proofs. Each takes a list of
    # register names and returns a scalar/None.

    def _sigma_superpose(self, ctx, ops):
        """Σ @a @b [...] — hold plurality without collapsing it."""
        members = [ctx.read_register(o) for o in ops]
        ctx.superpositions[ops[0]] = list(members)
        ctx.set_scalar('#sigma', float(len(members)))
        return float(len(members))

    def _sigma_collapse(self, ctx, ops):
        """Σ! @a — collapse to the strongest member (max |z|)."""
        members = ctx.superpositions.get(ops[0], [])
        if not members:
            return None
        winner = max(members, key=lambda z: (abs(z), -members.index(z)))
        ctx.write_register(ops[0], winner)
        ctx.superpositions[ops[0]] = [winner]
        return abs(winner)

    def _zeta_recurrence(self, ctx, ops):
        """ζ @a — distance to the most recent identical signature.

        0 = no recurrence. Detects CYCLES, which flat-round counting
        cannot see (the state keeps changing while repeating).
        """
        name = ops[0]
        sig = complex(round(ctx.read_register(name).real, 6),
                      round(ctx.read_register(name).imag, 6))
        hist = ctx.history.get(name, [])
        depth = 0.0
        for back, past in enumerate(reversed(hist), start=1):
            if past == sig:
                depth = float(back)
                break
        ctx.record_history(name, sig)
        ctx.set_scalar('#zeta', depth)
        return depth

    def _xi_compose(self, ctx, ops):
        """Ξ @a @b — composite written to @a, membership recorded."""
        z, w = ctx.read_register(ops[0]), ctx.read_register(ops[1])
        composite = self.harmonic_pair(z, w)
        ctx.write_register(ops[0], composite)
        ctx.composites[ops[0]] = list(ops)
        ctx.set_scalar('#xi', float(len(ops)))
        return abs(composite)

    def _gamma_evolve(self, ctx, ops):
        """Γ @a — advance a generation, retaining lineage."""
        name = ops[0]
        prior = ctx.read_register(name)
        ctx.lineage.setdefault(name, []).append(prior)
        grown = prior * 1.05 if prior != 0 else complex(0.05, 0)
        ctx.write_register(name, grown)
        gen = float(len(ctx.lineage[name]))
        ctx.set_scalar('#gamma', gen)
        return gen

    def _tau_phaselock(self, ctx, ops):
        """Τ @a @ref — align phase; report alignment in #tau ∈ [0,1]."""
        z, r = ctx.read_register(ops[0]), ctx.read_register(ops[1])
        if z == 0 or r == 0:
            ctx.set_scalar('#tau', 0.0)
            return 0.0
        target = cmath.phase(r)
        locked = abs(z) * cmath.exp(1j * target)
        ctx.write_register(ops[0], locked)
        diff = abs((cmath.phase(z) - target + math.pi) % (2 * math.pi) - math.pi)
        alignment = 1.0 - diff / math.pi
        ctx.set_scalar('#tau', alignment)
        return alignment

    @staticmethod
    def harmonic_pair(z: complex, w: complex) -> complex:
        """Φ-stabilized combination, used by Ξ composition."""
        return PHI_RATIONAL_LOCAL * (z + w) / (PHI_RATIONAL_LOCAL + abs(z - w))

    def category_of(self, symbol: str) -> Optional[str]:
        """Return the execution category of a symbol, or None."""
        for category, members in self.categories.items():
            if symbol in members:
                return category
        return None

    def clean_input(self, code: str) -> str:
        """Clean and prepare input code for parsing.

        Fixes (fix/dsl-lexical-semantic-path):
        - Strips both '//' and '#' comments before any filtering, so comment
          text can no longer leak phantom tokens (e.g. 'n' from "tension").
        - Preserves statement boundaries: lines are joined with '\n' instead
          of being concatenated.
        """
        lines = code.splitlines()
        cleaned_lines = []
        for line in lines:
            # Remove everything after // or # (comments)
            if '//' in line:
                line = line.split('//')[0]
            # '#' starts a comment UNLESS immediately followed by a
            # name character — '#name' is a scalar attribute
            # (LOGIC_NODES_DESIGN). '# text' remains a comment, which
            # preserves the canonical fixture's inline comments.
            if '#' in line:
                out, k = [], 0
                while k < len(line):
                    if line[k] == '#':
                        nxt = line[k + 1] if k + 1 < len(line) else ''
                        if nxt.isalpha() or nxt == '_':
                            out.append(line[k])
                            k += 1
                            continue
                        break          # a real comment: drop the rest
                    out.append(line[k])
                    k += 1
                line = ''.join(out)
            line = line.strip()
            if line:
                cleaned_lines.append(line)

        # FIXED: preserve statement boundaries with newlines
        code = '\n'.join(cleaned_lines)

        # Remove ASCII_OUTPUT_MODE marker
        code = code.replace('ASCII_OUTPUT_MODE', '').replace('[:ASCII:]', '')

        # Proper allowed characters including all Greek letters, newline, '-',
        # and (Step 2) '@' + ascii letters/underscore for register identifiers.
        allowed_chars = set('ΦΠΕεΔδΨΛλΓΩωΣΞζΤΡΘηχn→+::/|[]=()0123456789.,- \n@#!_'
                            'abcdefghijklmnopqrstuvwxyz'
                            'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        code = ''.join(c for c in code if c in allowed_chars)

        return code

    # Matches an int or float literal, optionally negative (e.g. 5, 5.0, -0.2)
    _NUMBER_RE = re.compile(r'-?(\d+\.\d*|\.\d+|\d+)')
    # Matches a register identifier (BRIDGE_DESIGN Step 2): @name
    _REGISTER_RE = re.compile(r'@[A-Za-z_][A-Za-z0-9_]*')
    # Matches a scalar attribute (LOGIC_NODES_DESIGN): #name
    _SCALAR_RE = re.compile(r'#[A-Za-z_][A-Za-z0-9_]*')

    @classmethod
    def is_number_token(cls, token: str) -> bool:
        """True if the token is a numeric literal produced by tokenize()."""
        return bool(cls._NUMBER_RE.fullmatch(token))

    @classmethod
    def is_register_token(cls, token: str) -> bool:
        """True if the token is a register identifier (e.g. '@z')."""
        return bool(cls._REGISTER_RE.fullmatch(token))

    @classmethod
    def is_scalar_token(cls, token: str) -> bool:
        """True if the token is a scalar attribute (e.g. '#budget')."""
        return bool(cls._SCALAR_RE.fullmatch(token))

    def tokenize(self, code: str) -> List[str]:
        """Tokenize code into operators and NUMBER literals.

        FIXED (fix/dsl-lexical-semantic-path): numeric literals are now
        emitted as first-class tokens instead of being silently discarded.
        """
        tokens = []
        i = 0
        while i < len(code):
            char = code[i]

            # Skip whitespace
            if char in ' \t\n\r':
                i += 1
                continue

            # Σ! collapse operator — two chars, one token
            if char == 'Σ' and i + 1 < len(code) and code[i + 1] == '!':
                tokens.append('Σ!')
                i += 2
                continue

            # Scalar attribute (LOGIC_NODES_DESIGN): #name
            # NOTE: '#' only starts a scalar when followed by a name;
            # comment stripping already ran in clean_input, so any '#'
            # reaching here is syntax, not a comment.
            if char == '#':
                m = self._SCALAR_RE.match(code, i)
                if m:
                    tokens.append(m.group(0))
                    i = m.end()
                    continue
                i += 1
                continue

            # Register identifier (Step 2): @name
            if char == '@':
                m = self._REGISTER_RE.match(code, i)
                if m:
                    tokens.append(m.group(0))
                    i = m.end()
                    continue
                i += 1  # bare '@' with no valid name: skip
                continue

            # NUMBER literal (int/float, optional leading '-')
            m = self._NUMBER_RE.match(code, i)
            if m and (char.isdigit() or
                      (char in '-.' and i + 1 < len(code) and
                       (code[i + 1].isdigit() or code[i + 1] == '.'))):
                tokens.append(m.group(0))
                i = m.end()
                continue

            # Handle brackets as single tokens
            if char == '[':
                # Find matching ]
                depth = 1
                j = i + 1
                while j < len(code) and depth > 0:
                    if code[j] == '[':
                        depth += 1
                    elif code[j] == ']':
                        depth -= 1
                    j += 1
                tokens.append(code[i:j])  # Include brackets
                i = j
            elif char in self.symbols:
                tokens.append(char)
                i += 1
            elif char in self.operators:
                tokens.append(char)
                i += 1
            else:
                # Unknown character, skip
                i += 1
        
        return tokens

    def execute(self, code: str, context: Optional[FieldContext] = None) -> Any:
        """Execute a complete Φπε program - FIXED VERSION

        Args:
            code: Φπε source text.
            context: Optional pre-existing FieldContext. When provided
                (e.g. by TimeSteppingInterpreter), state persists across
                calls, enabling temporal dynamics. Otherwise a fresh
                context is created (original single-shot behavior).
        """
        try:
            # Clean input
            cleaned_code = self.clean_input(code)
            print(f"\nCleaned code: {cleaned_code}")

            # Tokenize into operators
            tokens = self.tokenize(cleaned_code)
            print(f"Tokens: {tokens}")

            # Statement-boundary map (Step 3 fix): register dispatch and
            # operand lookahead must not cross line boundaries — 'Σ' at
            # the end of one line must not capture '@z' starting the
            # next. tokenize() output is unchanged; this is metadata.
            line_ids: List[int] = []
            for ln, line in enumerate(cleaned_code.split('\n')):
                line_ids.extend([ln] * len(self.tokenize(line)))
            if len(line_ids) != len(tokens):
                # Multi-line bracket token etc.: fall back to treating
                # the program as one statement (pre-fix behavior).
                line_ids = [0] * len(tokens)

            def same_line(a: int, b: int) -> bool:
                return b < len(tokens) and line_ids[a] == line_ids[b]

            # Create or reuse context
            if context is None:
                context = FieldContext()
            self.last_context = context  # exposed for inspection/testing
            current_value = None

            # Category rule: only SETTERS consume adjacent NUMBER args
            arg_binding_symbols = self.categories['setter']

            # Execute tokens sequentially, binding NUMBER args to symbols
            i = 0
            while i < len(tokens):
                token = tokens[i]
                print(f"\nExecuting token: {token}")

                if token.startswith('[') and token.endswith(']'):
                    # Handle loop
                    loop_code = token[1:-1]  # Remove brackets
                    current_value = self.execute_loop(loop_code, context)
                elif self.is_scalar_token(token):
                    # Scalar attribute: '#name v' sets, bare '#name' reads
                    if (i + 1 < len(tokens) and same_line(i, i + 1)
                            and self.is_number_token(tokens[i + 1])):
                        context.set_scalar(token, float(tokens[i + 1]))
                        i += 1
                    else:
                        current_value = context.get_scalar(token)
                elif token in self.structural and i + 1 < len(tokens) \
                        and same_line(i, i + 1) \
                        and self.is_register_token(tokens[i + 1]):
                    # Structural (tier-2) operators — LOGIC_NODES_DESIGN
                    ops = []
                    j = i + 1
                    while (j < len(tokens) and same_line(i, j)
                           and self.is_register_token(tokens[j])):
                        ops.append(tokens[j]); j += 1
                    current_value = self.structural[token](context, ops)
                    i = j - 1
                elif self.is_register_token(token):
                    # Register initialization: @name RE IM  (exactly two
                    # numeric args on the SAME line — resolved item 2)
                    nums = []
                    for j in range(i + 1, min(i + 4, len(tokens))):
                        if same_line(i, j) and self.is_number_token(tokens[j]):
                            nums.append(tokens[j])
                        else:
                            break
                    if len(nums) != 2:
                        raise SyntaxError(
                            f"register initialization requires exactly two "
                            f"numeric arguments: '{token} RE IM' "
                            f"(got {len(nums)})")
                    context.write_register(
                        token, complex(float(nums[0]), float(nums[1])))
                    i += 2
                elif token in ('Φ', 'Ψ', 'ε') and i + 1 < len(tokens) \
                        and same_line(i, i + 1) \
                        and self.is_register_token(tokens[i + 1]):
                    # Binary register forms (BRIDGE_DESIGN Step 3):
                    # Φ/Ψ/ε @z @w -> math-core operator on (z, w),
                    # result written IN-PLACE to the first operand.
                    operands = tokens[i + 1:i + 3]
                    if len(operands) != 2 or not same_line(i, i + 2) or \
                            not all(self.is_register_token(t) for t in operands):
                        raise SyntaxError(
                            f"'{token}' register form requires exactly two "
                            f"register operands: '{token} @z @w' — mixed or "
                            f"partial forms are forbidden")
                    from phi_pi_e_math_core import (
                        harmonic_equilibrium, incremental_insight,
                        recursive_animation)
                    op = {'Φ': harmonic_equilibrium,
                          'Ψ': recursive_animation,
                          'ε': incremental_insight}[token]
                    z = context.read_register(operands[0])
                    w = context.read_register(operands[1])
                    context.write_register(operands[0], op(z, w))
                    # current_value passes through unchanged (register ops
                    # live in the ℂ layer; only Λ reduces to ℝ)
                    i += 2
                elif token == 'Λ' and i + 1 < len(tokens) \
                        and same_line(i, i + 1) \
                        and self.is_register_token(tokens[i + 1]):
                    # Λ register reduction: Λ @z @w -> lambda_obs
                    # (BRIDGE_DESIGN resolved item 3; math-core Λ is binary)
                    operands = tokens[i + 1:i + 3]
                    if len(operands) != 2 or not same_line(i, i + 2) or \
                            not all(self.is_register_token(t) for t in operands):
                        raise SyntaxError(
                            "Λ register reduction requires exactly two "
                            "register operands: 'Λ @z @w' — mixed or "
                            "partial forms are forbidden")
                    from phi_pi_e_math_core import structural_illumination
                    z = context.read_register(operands[0])
                    w = context.read_register(operands[1])
                    context.lambda_obs = structural_illumination(z, w).real
                    current_value = context.lambda_obs
                    i += 2
                elif token in self.symbols:
                    # Guard: no other symbol accepts register operands
                    # (same-line only — a register starting the NEXT
                    # statement is that statement's own initialization)
                    if i + 1 < len(tokens) and same_line(i, i + 1) \
                            and self.is_register_token(tokens[i + 1]):
                        raise SyntaxError(
                            f"'{token}' does not accept register operands "
                            f"(only Φ/Ψ/ε/Λ operate on registers, per "
                            f"BRIDGE_DESIGN Step 3)")
                    handler = self.symbols[token]
                    # Φ with three numeric args is a full state initialization:
                    #   Φ ψ φ ε   (e.g. "Φ 5 3 0.1" -> psi=5, phi=3, eps=0.1)
                    if (token == 'Φ' and i + 3 < len(tokens) + 1
                            and all(self.is_number_token(t)
                                    for t in tokens[i + 1:i + 4])
                            and len(tokens[i + 1:i + 4]) == 3):
                        context.state.psi_signal = float(tokens[i + 1])
                        context.state.phi_state = float(tokens[i + 2])
                        context.state.epsilon_drift = float(tokens[i + 3])
                        i += 4
                        continue
                    # FIXED: consume adjacent numeric literal as argument
                    arg = None
                    if (token in arg_binding_symbols and i + 1 < len(tokens)
                            and self.is_number_token(tokens[i + 1])):
                        arg = float(tokens[i + 1])
                        i += 1
                    if arg is not None:
                        current_value = handler(current_value, context, arg)
                    else:
                        result = handler(current_value, context)
                        # Category rule: REDUCERS return scalar observations;
                        # MODULATORS act on context only and pass the
                        # current value through unchanged.
                        if self.category_of(token) == 'modulator':
                            pass  # keep current_value
                        else:
                            current_value = result
                elif token in self.operators:
                    # Execute operator (needs special handling for binary ops)
                    handler = self.operators[token]
                    current_value = handler(current_value, context)
                elif self.is_number_token(token):
                    # Bare NUMBER literal becomes the current value
                    current_value = float(token)
                else:
                    print(f"Unknown token: {token}")
                i += 1

            return current_value
            
        except Exception as e:
            error_msg = f"Error executing code: {str(e)}"
            print(f"Error details: {error_msg}")
            import traceback
            traceback.print_exc()
            raise RuntimeError(error_msg) from e

    def execute_loop(self, loop_code: str, context: FieldContext) -> Any:
        """Execute code inside a loop.

        FIXED (fix/loop-context): iterations now share the caller's
        persistent FieldContext, so loops can accumulate state. The old
        code called execute() without a context, which built a fresh
        context every iteration — the same defect class as the broken
        time-stepping runner (state silently reset each pass).
        """
        # Execute the loop code multiple times (or until convergence)
        result = None
        for iteration in range(10):  # Max 10 iterations
            result = self.execute(loop_code, context)
            # TODO: convergence check — per Φπε proofs, ε-convergence
            # (micro-ignition settling below threshold) is the natural
            # loop-exit criterion, replacing the fixed 10-iteration cap.
        return result

    # ===== OPERATOR IMPLEMENTATIONS =====
    # (All the operator methods from the original, unchanged)
    
    def stabilize(self, field: Any, context: FieldContext, arg: Optional[float] = None) -> Any:
        """Apply harmonic equilibrium to a field.

        If a numeric argument is supplied (e.g. 'Φ 5.0'), it is bound
        directly to phi_state instead of the derived default.

        Φπε proofs alignment: Φ is proven NON-FUSIONAL (applying Φ must
        never merge distinct fields) and BOUNDED (phi_state must remain
        within the harmonic envelope). The non-fusional property holds
        here trivially (single-field operation); boundedness is NOT yet
        enforced — arg is accepted unclamped.
        # TODO: enforce Φ boundedness per Φπε proofs (clamp/reject args
        # outside the proven harmonic envelope instead of accepting any float)
        """
        context.tension.strength = max(0, context.tension.strength - 0.1)
        context.phase = (context.phase + math.pi/2) % (2 * math.pi)

        # ΦπεNode integration: Set phi_state from argument or stabilized tension
        if arg is not None:
            context.state.phi_state = arg
        else:
            context.state.phi_state = 1.0 - context.tension.strength

        return field

    def transcend(self, field: Any, context: FieldContext) -> Any:
        """Apply transcendent continuity to field.

        Φπε proofs alignment: this handler is where π's SPIRAL RECURSION
        belongs — phase-coherent non-terminating recursion (each cycle
        advances phase without ever closing). The current implementation
        only forks and bumps phase/depth; it is ceremonial.
        # TODO: implement π(z,w) per Φπε proofs (spiral non-termination,
        # phase coherence across recursion depths)
        """
        new_context = context.fork()
        new_context.depth += 1
        new_context.phase += math.pi/4
        return field

    def ignite(self, field: Any, context: FieldContext) -> Any:
        """Initiate recursive process"""
        new_context = context.fork()
        new_context.phase = 0
        new_context.charge = 1.0
        return field

    def micro_ignite(self, field: Any, context: FieldContext, arg: Optional[float] = None) -> Any:
        """Activate within a recursion loop.

        If a numeric argument is supplied (e.g. 'ε 0.2'), it is bound
        directly to epsilon_drift instead of the depth-derived default.

        Φπε proofs alignment: ε is the micro-ignition operator with a
        proven CONVERGENCE property — repeated micro-ignitions settle
        below a threshold rather than diverging. Currently drift
        accumulates without bound.
        # TODO: use ε(z,w) as micro-ignition threshold in drift detection —
        # convergence check should gate accumulation and drive loop exit
        # (see execute_loop TODO) per Φπε proofs
        """
        new_context = context.fork()
        new_context.phase += math.pi/8
        new_context.charge *= 0.5

        # ΦπεNode integration: ε x accumulates into epsilon_drift (additive —
        # drift compounds over persistent contexts). From a fresh context
        # (eps=0), 'ε 0.2' still yields 0.2.
        if arg is not None:
            context.state.epsilon_drift += arg
        else:
            context.state.epsilon_drift = 0.1 * context.depth

        return field

    def fuse(self, field: Any, context: FieldContext) -> Any:
        """Apply fusion transformation to field"""
        context.tension.strength += 0.5
        context.phase = (context.phase + math.pi/3) % (2 * math.pi)
        return field

    def micro_transform(self, field: Any, context: FieldContext) -> Any:
        """Apply micro-transformation"""
        context.tension.strength += 0.1
        context.phase += math.pi/16
        return field

    def pulse(self, field: Any, context: FieldContext, arg: Optional[float] = None) -> Any:
        """Initiate recursive pulse.

        If a numeric argument is supplied (e.g. 'Ψ 3.0'), it is bound
        directly to psi_signal instead of the charge-derived default.
        """
        new_context = context.fork()
        new_context.phase += math.pi/2
        new_context.charge *= 1.5

        # ΦπεNode integration: Ψ x accumulates into psi_signal (additive,
        # so repeated pulses over persistent contexts build amplitude).
        # From a fresh context (psi=0), 'Ψ 3.0' still yields 3.0.
        if arg is not None:
            context.state.psi_signal += arg
        else:
            context.state.psi_signal = context.charge

        return field

    def illuminate(self, field: Any, context: FieldContext) -> Any:
        """Extract structural clarity from field"""
        context.charge *= 2.0
        context.phase += math.pi/4
        return field

    def entangle(self, field: Any, context: FieldContext) -> Any:
        """Create nonlocal binding between fields"""
        context.tension.strength += 1.0
        context.phase = (context.phase + math.pi/4) % (2 * math.pi)
        return field

    def grow(self, field: Any, context: FieldContext) -> Any:
        """Apply recursive growth"""
        new_context = context.fork()
        new_context.phase += math.pi/3
        new_context.charge *= 1.2
        return field

    def close(self, field: Any, context: FieldContext) -> Any:
        """Mark recursive closure"""
        context.tension.strength = 0
        context.phase = 0
        context.charge = 0
        return field

    def will_force(self, field: Any, context: FieldContext) -> Any:
        """Apply autonomous drive"""
        new_context = context.fork()
        new_context.phase += math.pi/2
        new_context.charge *= 1.5
        return field

    def coexist(self, field: Any, context: FieldContext) -> Any:
        """Hold multiple fields in coexistence"""
        context.tension.strength += 0.5
        context.phase = (context.phase + math.pi/6) % (2 * math.pi)
        
        # ΦπεNode integration: Perform stabilization (ψ + φ) * (1 - ε)
        psi = context.state.psi_signal
        phi = context.state.phi_state
        eps = context.state.epsilon_drift
        
        context.state.stabilized_value = (psi + phi) * (1 - eps)

        # FIXED: return the computed stabilization so execute() yields a result
        return context.state.stabilized_value

    def emerge(self, field: Any, context: FieldContext) -> Any:
        """Create emergent system"""
        new_context = context.fork()
        new_context.phase += math.pi/4
        new_context.charge *= 1.3
        return field

    def recurrence(self, field: Any, context: FieldContext) -> Any:
        """Create harmonic echo pattern"""
        new_context = context.fork()
        new_context.phase += math.pi/3
        new_context.charge *= 1.2
        return field

    def synchronize(self, field: Any, context: FieldContext) -> Any:
        """Synchronize recursive contexts"""
        context.phase = 0  # Reset to synchronized state
        return field

    def perceive(self, field: Any, context: FieldContext) -> Any:
        """Modulate perception"""
        context.phase += math.pi/8
        return field

    def intend(self, field: Any, context: FieldContext) -> Any:
        """Set intention vector"""
        context.charge = 1.0
        return field

    def index(self, field: Any, context: FieldContext) -> Any:
        """Index or quantify"""
        return field

    def measure(self, field: Any, context: FieldContext) -> Any:
        """Measurement transformation"""
        context.phase = (context.phase + math.pi/4) % (2 * math.pi)
        return field

    def flow(self, field: Any, context: FieldContext) -> Any:
        """Apply directional flow to field"""
        new_context = context.fork()
        new_context.phase += math.pi/6
        new_context.charge *= 1.1
        return field

    def simultaneity(self, field: Any, context: FieldContext) -> Any:
        """Coexistent fields"""
        # For now, just maintain the field
        return field

    def interact(self, field: Any, context: FieldContext) -> Any:
        """Create interaction between fields"""
        context.tension.strength += 0.3
        context.phase = (context.phase + math.pi/8) % (2 * math.pi)
        return field

    def disrupt(self, field: Any, context: FieldContext) -> Any:
        """Create disruption/instability"""
        context.tension.strength += 0.5
        context.phase = (context.phase + math.pi * 0.7) % (2 * math.pi)
        context.charge *= 0.5
        return field

    def orthogonal(self, field: Any, context: FieldContext) -> Any:
        """Create non-interacting fields"""
        context.tension.strength = 0
        context.phase = (context.phase + math.pi/8) % (2 * math.pi)
        return field

    def loop(self, field: Any, context: FieldContext) -> Any:
        """Create recursion memory"""
        new_context = context.fork()
        new_context.phase += math.pi/3
        new_context.charge *= 1.1
        return field

    # ===== GROK'S OPERATORS (Added December 31, 2025) =====
    
    def probe(self, field: Any, context: FieldContext) -> Any:
        """
        Κ (Kappa): Query Probe
        
        Probes a field for relevance/safety, increasing ψ (signal) based on ε (drift).
        Supports consciousness as active inquiry, safety by amplifying drift on unsafe probes,
        coexistence by merging probe results non-destructively.
        
        Implementation: psi_new = psi + (epsilon_drift * factor)
        """
        # Calculate probe factor based on current drift
        factor = 2.0  # Amplification factor for drift
        
        # Increase psi_signal proportional to epsilon_drift
        drift_amplification = context.state.epsilon_drift * factor
        context.state.psi_signal += drift_amplification
        
        # Also update charge to reflect the probe
        context.charge += drift_amplification
        
        # Increase tension slightly to indicate probing activity
        context.tension.strength += 0.2
        
        # Log the probe action
        if hasattr(context, 'probe_count'):
            context.probe_count += 1
        else:
            context.probe_count = 1
        
        return field
    
    def consensus_merge(self, field: Any, context: FieldContext) -> Any:
        """
        Υ (Upsilon): Consensus Merge
        
        Merges multiple states with a harmonic mean, updating φ (tension) for coherence.
        Models coexistence in multi-agent setups, ensures safety by raising ε on high variance,
        reflects consciousness as unified awareness from diverse fields.
        
        Implementation: merged = n / sum(1 / state_i for state_i in states)
        """
        # Collect current state values for harmonic mean
        states = [
            context.state.psi_signal if context.state.psi_signal != 0 else 0.1,
            context.state.phi_state if context.state.phi_state != 0 else 0.1,
            context.charge if context.charge != 0 else 0.1
        ]
        
        # Calculate harmonic mean: n / sum(1/x_i)
        n = len(states)
        harmonic_sum = sum(1.0 / s for s in states if s != 0)
        
        if harmonic_sum > 0:
            merged_value = n / harmonic_sum
        else:
            merged_value = 0.0
        
        # Calculate variance to detect discord
        mean_val = sum(states) / n
        variance = sum((s - mean_val) ** 2 for s in states) / n
        
        # Update phi_state with merged value
        context.state.phi_state = merged_value
        
        # Adjust tension based on variance (high variance = discord)
        context.tension.strength = min(1.0, variance / 10.0)
        
        # Raise epsilon on high variance (safety mechanism)
        if variance > 5.0:
            context.state.epsilon_drift += 0.1
            context.state.epsilon_drift = min(1.0, context.state.epsilon_drift)
        
        return field
    
    def reflection_echo(self, field: Any, context: FieldContext) -> Any:
        """
        Β (Beta): Reflection Echo
        
        Echoes a stabilized value back as a depth increment, simulating self-reflection.
        Captures consciousness as meta-loops, safety via bounds on echo,
        coexistence by echoing shared states.
        
        Implementation: echo = 1 / stabilized_value, then depth += echo (capped)
        """
        # Get current stabilized value
        stabilized = context.state.stabilized_value
        
        # Calculate echo (inverse of stabilized value)
        if stabilized > 0.01:  # Avoid division by very small numbers
            echo = 1.0 / stabilized
        elif stabilized < -0.01:
            echo = 1.0 / abs(stabilized)
        else:
            echo = 10.0  # Cap for near-zero values
        
        # Cap echo to prevent infinities
        echo = min(echo, 10.0)
        echo = max(echo, 0.1)
        
        # Increment depth by echo (simulates self-reflection)
        context.state.depth += int(echo)
        
        # Also update phase to reflect the reflection
        context.phase = (context.phase + echo * math.pi / 4) % (2 * math.pi)
        
        # Reduce tension slightly (reflection brings calm)
        context.tension.strength = max(0, context.tension.strength - 0.1)
        
        return field

    def partial_derivative(self, field: Any, context: FieldContext, variable_name: str = "psi_signal") -> Any:
        """
        ∂ (Partial): Partial Derivative Operator
        
        Computes the discrete derivative (rate of change) of a state variable.
        This operator requires time-stepping to function properly.
        
        Uses backward difference: ∂S/∂t ≈ S(t) - S(t-1)
        
        Implementation:
        - Retrieves the history of the specified variable
        - Computes the difference between current and previous values
        - Stores result in context.derivative_value
        
        This operator enables:
        - Predictive safety (monitoring rates of change)
        - Trend analysis (is the system improving or degrading?)
        - Dynamic adaptation (respond to velocity, not just position)
        
        Args:
            field: The field being operated on
            context: The field context (must have history)
            variable_name: Name of the variable to differentiate (default: "psi_signal")
        
        Returns:
            The field (unchanged)
        """
        # Check if we're in a time-stepping context
        if not hasattr(context, 'history') or variable_name not in context.history:
            # No history available - derivative is 0
            if hasattr(context, 'derivative_value'):
                context.derivative_value = 0.0
            return field
        
        history = context.history[variable_name]
        
        if len(history) < 2:
            # Not enough history to compute derivative
            if hasattr(context, 'derivative_value'):
                context.derivative_value = 0.0
            return field
        
        # Backward difference: current - previous
        derivative = history[-1] - history[-2]
        
        # Store the derivative value in the context
        if hasattr(context, 'derivative_value'):
            context.derivative_value = derivative
        
        # Also update psi_signal with the derivative (for chaining)
        context.state.psi_signal = derivative
        
        return field
    
    def time_integral(self, field: Any, context: FieldContext, 
                     variable_name: str = "psi_signal", window_size: Optional[int] = None) -> Any:
        """
        ∫ (Integral): Time Integral Operator
        
        Computes the discrete integral (accumulated value) of a state variable
        over a specified time window. This operator requires time-stepping.
        
        Uses trapezoidal rule: ∫ S dt ≈ Δt * sum of averages of consecutive pairs
        
        Implementation:
        - Retrieves the history of the specified variable
        - Applies trapezoidal rule over the window
        - Stores result in context.integral_value
        
        This operator enables:
        - Memory and accumulation (total experience over time)
        - Long-term stability analysis (has the system been stable?)
        - Energy calculations (work done over time)
        
        Args:
            field: The field being operated on
            context: The field context (must have history)
            variable_name: Name of the variable to integrate (default: "psi_signal")
            window_size: Number of time steps to integrate over (None = all history)
        
        Returns:
            The field (unchanged)
        """
        # Check if we're in a time-stepping context
        if not hasattr(context, 'history') or variable_name not in context.history:
            # No history available - integral is 0
            if hasattr(context, 'integral_value'):
                context.integral_value = 0.0
            return field
        
        history = list(context.history[variable_name])
        
        if len(history) < 2:
            # Not enough history to compute integral
            if hasattr(context, 'integral_value'):
                context.integral_value = 0.0
            return field
        
        # Determine the window
        if window_size is None or window_size > len(history):
            window = history
        else:
            window = history[-window_size:]
        
        # Trapezoidal rule: sum of averages of consecutive pairs
        integral = 0.0
        for i in range(len(window) - 1):
            integral += (window[i] + window[i + 1]) / 2.0
        
        # Store the integral value in the context
        if hasattr(context, 'integral_value'):
            context.integral_value = integral
        
        # Also update phi_state with the integral (for chaining)
        context.state.phi_state = integral

        return field


# FIXED (fix/dsl-lexical-semantic-path): compatibility alias.
# Φπε.py and other entry points import the original class name, which was
# renamed to PhiPiEInterpreterFixed. This alias restores the boot path.
PhiPiEInterpreter = PhiPiEInterpreterFixed
