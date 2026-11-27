# Optional Omega Translation Bridge (`harmonia_omega_bridge.py`)

`harmonia_omega_bridge.py` is a thin, **zero-dependency** Python bridge
between Andrew Josef Kadziolka's authoritative complex math core
(`phi_pi_e_math_core.py`) and an optional native pure seeded-OM-2 Omega
runtime binary (`harmonia-om-macos` on Apple Silicon macOS or
`harmonia-om-linux` on AArch64 Linux).

## Design Guarantees

- **Zero edits to `phi_pi_e_math_core.py` or `phi_pi_e_interpreter.py`:**
  The math core remains pure on ℂ, and all existing `INVARIANTS.md`
  semantics (including `Φ 5.0 / Ψ 3.0 / ε 0.2 / Σ → 6.4`) are untouched.
- **Zero external dependencies:** Uses only the Python standard library
  (`hashlib`, `json`, `math`, `platform`, `shutil`, `struct`, `subprocess`).
- **Safe automatic fallback:** When no native binary is installed (for
  example in CI or standard Python environments), `HarmoniaOmegaBridge`
  dispatches cleanly to `phi_pi_e_math_core.py` and emits identical
  `HARMONIA-OM2-RECEIPT-V1` FIPS 180-4 SHA-256 execution receipts.
- **Fail-closed categorical boundary:** `Ω` (Theorem 3.2, Qualia Gateway)
  refuses numerical evaluation with status `1000001` (`categorical_omega`
  raises `CategoricalBoundaryError` / `OmegaBoundaryRefusal`), and `π(z, 0)`
  raises `ValueError` with status `1000002`.
- **Tamper-evident receipts:** Native subprocess JSON receipts are verified
  against `SHA-256(receipt_preimage)` before returning (`OmegaReceiptTamperError`
  on mismatch).

## Binary Discovery

`find_harmonia_binary()` checks, in order:
1. Explicit `binary_path` argument passed to `HarmoniaOmegaBridge(binary_path=...)`
2. `HARMONIA_OMEGA_BIN` environment variable (`""` disables native lookup and forces fallback)
3. `./bin/<harmonia-om-macos|harmonia-om-linux>` relative to the repository or CWD
4. `~/workspace/omega-harmonia/bin/<harmonia-om-macos|harmonia-om-linux>`
5. `PATH` (`harmonia-om-macos`, `harmonia-om-linux`, or `harmonia-om`)

## Status Codes

| Status | Meaning |
|---|---|
| `0` | `OK` — numerical operator, corridor, or governance check passed |
| `1000001` | `Ω` Theorem 3.2 categorical boundary refusal |
| `1000002` | `π(z, 0)` singularity refusal |
| `1000003` | `π` recursion depth `n < 1` refusal |
| `1000004` | Non-finite / floating-point overflow refusal |
| `1000011` | `\|` disjoint sector check failed (overlap or zero mask) |
| `1000012` | `[]` recursion depth exceeded ceiling (`< 1` or `depth > ceiling`) |
| `1000013` | `->` cyclic progression detected |
| `1000014` | `=` lock invariant violated |
| `1000015` | SHA-256 receipt tamper check failed |
| `1000099` | Invalid, non-finite, or oversized CLI arguments |

## Quick Usage

```python
from harmonia_omega_bridge import HarmoniaOmegaBridge

bridge = HarmoniaOmegaBridge()
corridor = bridge.eval_corridor(5.0, 3.0, 0.2)
assert corridor.value == 6.4
assert bridge.verify_receipt(corridor.receipt_preimage, corridor.sha256)

phi = bridge.eval_operator("Φ", 3 + 4j, 1 - 2j)
omega = bridge.eval_operator("Ω", 1 + 1j, 2 - 1j)
assert not omega.ok and omega.status == 1000001
```
