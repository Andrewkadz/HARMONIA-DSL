"""Pure mathematical topology and lattice utilities for Harmonia.

Modules in this package are intentionally independent of the interpreter and
swarm layers. They provide testable geometric substrates only; any application
to governance or DSL semantics requires a separate, explicit design decision.
"""

from .e8_lattice import (
    COVERING_RADIUS_SQUARED,
    DIMENSION,
    first_shell,
    is_lattice_point,
    nearest_point,
    quantization_error_squared,
    shell_index,
    squared_norm,
)

__all__ = [
    "COVERING_RADIUS_SQUARED",
    "DIMENSION",
    "first_shell",
    "is_lattice_point",
    "nearest_point",
    "quantization_error_squared",
    "shell_index",
    "squared_norm",
]
