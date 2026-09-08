"""Pure mathematical utilities for the real E8 lattice.

The E8 lattice is represented in its standard coordinate realization:

    E8 = D8 ∪ (D8 + (1/2, ..., 1/2))

where D8 contains integer vectors whose coordinate sum is even.  Thus an E8
vector has either all integral coordinates with even sum, or all half-integral
coordinates with even sum.

This module intentionally has no dependency on the Harmonia interpreter, the
swarm layer, or third-party packages.  It exposes only standard lattice
operations that can be verified independently:

- membership;
- exact nearest-point quantization using the D8 and shifted-D8 candidates;
- shell indexing by squared norm;
- generated first-shell roots.

The implementation uses a numerical tolerance only at the public boundary so
that ordinary floating-point vectors representing integral or half-integral
coordinates are accepted.  Generated lattice points remain exact binary
halves/integers.
"""

from __future__ import annotations

from itertools import combinations, product
from math import isclose
from typing import Iterable, Sequence, Tuple


DIMENSION = 8
HALF = 0.5
DEFAULT_TOLERANCE = 1e-9
COVERING_RADIUS_SQUARED = 1.0

Vector = Tuple[float, ...]


def _as_vector(vector: Sequence[float] | Iterable[float]) -> Vector:
    """Coerce an input to a finite-dimensional E8 candidate vector."""
    result = tuple(float(value) for value in vector)
    if len(result) != DIMENSION:
        raise ValueError(f"E8 vectors must have exactly {DIMENSION} coordinates")
    return result


def _nearest_integer(value: float) -> int:
    """Return a deterministic nearest integer; ties use Python's even rule."""
    return int(round(value))


def _is_close_to_integer(value: float, tolerance: float) -> bool:
    return isclose(value, _nearest_integer(value), abs_tol=tolerance)


def _squared_distance(left: Vector, right: Vector) -> float:
    return sum((a - b) ** 2 for a, b in zip(left, right))


def squared_norm(vector: Sequence[float] | Iterable[float]) -> float:
    """Return the Euclidean squared norm of an 8-dimensional vector."""
    v = _as_vector(vector)
    return sum(value * value for value in v)


def is_lattice_point(
    vector: Sequence[float] | Iterable[float], *, tolerance: float = DEFAULT_TOLERANCE
) -> bool:
    """Return whether ``vector`` belongs to the standard E8 lattice.

    Membership has two disjoint coordinate classes:

    1. all coordinates integral and their sum even; or
    2. all coordinates half-integral and their sum even.
    """
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    v = _as_vector(vector)

    if all(_is_close_to_integer(value, tolerance) for value in v):
        integral = tuple(_nearest_integer(value) for value in v)
        return sum(integral) % 2 == 0

    shifted = tuple(value - HALF for value in v)
    if all(_is_close_to_integer(value, tolerance) for value in shifted):
        base = tuple(_nearest_integer(value) for value in shifted)
        # For x = base + 1/2^8, sum(x) is even exactly when sum(base) is even.
        return sum(base) % 2 == 0

    return False


def _nearest_d8(vector: Vector) -> Vector:
    """Decode the nearest D8 point using parity-corrected coordinate rounding."""
    rounded = [_nearest_integer(value) for value in vector]
    if sum(rounded) % 2 == 0:
        return tuple(float(value) for value in rounded)

    # The independently nearest integer point has odd parity.  Changing one
    # coordinate by ±1 fixes parity; choose the least-cost such correction.
    best_index = 0
    best_value = rounded[0]
    best_cost = float("inf")
    for index, (value, integer) in enumerate(zip(vector, rounded)):
        for corrected in (integer - 1, integer + 1):
            cost = (value - corrected) ** 2
            candidate_key = (cost, index, corrected)
            best_key = (best_cost, best_index, best_value)
            if candidate_key < best_key:
                best_index, best_value, best_cost = index, corrected, cost

    rounded[best_index] = best_value
    return tuple(float(value) for value in rounded)


def nearest_point(vector: Sequence[float] | Iterable[float]) -> Vector:
    """Return a deterministic nearest E8 lattice point.

    E8 is the union of D8 and its all-half-coordinate translate.  The nearest
    point in each coset is decoded independently, then the closer candidate is
    selected.  In an exact tie, lexicographic ordering makes the result stable.
    """
    v = _as_vector(vector)
    integer_coset = _nearest_d8(v)
    shifted_input = tuple(value - HALF for value in v)
    shifted_base = _nearest_d8(shifted_input)
    half_coset = tuple(value + HALF for value in shifted_base)

    candidates = (integer_coset, half_coset)
    return min(candidates, key=lambda point: (_squared_distance(v, point), point))


def quantization_error_squared(vector: Sequence[float] | Iterable[float]) -> float:
    """Return the squared distance from a vector to its nearest E8 point."""
    v = _as_vector(vector)
    return _squared_distance(v, nearest_point(v))


def shell_index(
    point: Sequence[float] | Iterable[float], *, tolerance: float = DEFAULT_TOLERANCE
) -> int:
    """Return the shell index ``|point|² / 2`` for an E8 lattice point.

    E8 lattice norms are non-negative even integers.  Non-lattice inputs and
    values that violate this norm property are rejected rather than coerced.
    """
    p = _as_vector(point)
    if not is_lattice_point(p, tolerance=tolerance):
        raise ValueError("shell_index is defined only for E8 lattice points")
    norm_squared = squared_norm(p)
    index = int(round(norm_squared / 2.0))
    if index < 0 or not isclose(norm_squared, 2.0 * index, abs_tol=tolerance):
        raise ValueError("E8 lattice squared norm must be a non-negative even integer")
    return index


def first_shell() -> Tuple[Vector, ...]:
    """Generate the 240 E8 roots at squared norm 2.

    The roots consist of:

    - 112 vectors with two ±1 coordinates and the other six coordinates zero;
    - 128 all-half vectors whose number of negative signs is even.
    """
    roots = set()

    for left, right in combinations(range(DIMENSION), 2):
        for left_sign, right_sign in product((-1.0, 1.0), repeat=2):
            root = [0.0] * DIMENSION
            root[left] = left_sign
            root[right] = right_sign
            roots.add(tuple(root))

    for signs in product((-1.0, 1.0), repeat=DIMENSION):
        if sum(sign < 0.0 for sign in signs) % 2 == 0:
            roots.add(tuple(HALF * sign for sign in signs))

    return tuple(sorted(roots))
