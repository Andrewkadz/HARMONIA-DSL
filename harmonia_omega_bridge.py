"""Thin zero-dependency Python bridge for Pure Seeded OM-2 Harmonia core.

Calls the compiled native Omega binary (`harmonia-om-macos` on Apple Silicon
macOS or `harmonia-om-linux` on AArch64 Linux) for closed-form complex operators,
the scalar corridor Σ = (ψ + φ)(1 − ε), fail-closed Ω / π(z,0) refusals,
governance checks (|, [], ->, =), and FIPS 180-4 SHA-256 execution receipts.

When no native binary is installed (e.g. CI without omc), falls back cleanly
to pure Python `phi_pi_e_math_core.py` without modifying `phi_pi_e_math_core.py`.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import shutil
import struct
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Sequence, Union


STATUS_OK = 0
STATUS_OMEGA_BOUNDARY = 1000001
STATUS_PI_W_ZERO = 1000002
STATUS_PI_DEPTH_LT1 = 1000003
STATUS_OVERFLOW = 1000004
STATUS_GOV_PIPE_OVERLAP = 1000011
STATUS_GOV_BRACKET_DEPTH = 1000012
STATUS_GOV_ARROW_CYCLE = 1000013
STATUS_GOV_EQ_LOCK = 1000014
STATUS_RECEIPT_TAMPER = 1000015
STATUS_CLI_ERROR = 1000099


def _load_math_core():
    try:
        import phi_pi_e_math_core as core
        return core
    except ImportError:
        candidates = [
            Path(__file__).resolve().parent,
            Path(__file__).resolve().parent.parent,
        ]
        for cand in candidates:
            if (cand / "phi_pi_e_math_core.py").is_file():
                s = str(cand)
                if s not in sys.path:
                    sys.path.insert(0, s)
                import phi_pi_e_math_core as core
                return core
        raise


_MATH_CORE = None


def _core():
    global _MATH_CORE
    if _MATH_CORE is None:
        _MATH_CORE = _load_math_core()
    return _MATH_CORE


class OmegaReceiptTamperError(RuntimeError):
    """Raised when a receipt digest fails FIPS 180-4 SHA-256 verification."""


class OmegaBoundaryRefusal(TypeError):
    """Raised when Ω (Theorem 3.2) or a fail-closed boundary is invoked numerically."""

    def __init__(self, message: str, status: int = STATUS_OMEGA_BOUNDARY,
                 receipt: Optional["OmegaReceiptResult"] = None):
        super().__init__(message)
        self.status = status
        self.receipt = receipt


@dataclass(frozen=True)
class OmegaReceiptResult:
    ok: bool
    op: str
    status: int
    verdict: str
    reason: str
    value: Optional[Union[complex, float]]
    sha256: str
    receipt_preimage: str
    backend: str
    exit_code: int = 0
    real_bits: Optional[str] = None
    imag_bits: Optional[str] = None
    sigma_bits: Optional[str] = None
    abs_value: Optional[float] = None


def _platform_binary_name() -> Optional[str]:
    sysname = platform.system()
    machine = platform.machine().lower()
    if sysname == "Darwin" and machine in ("arm64", "aarch64"):
        return "harmonia-om-macos"
    if sysname == "Linux" and machine in ("aarch64", "arm64"):
        return "harmonia-om-linux"
    return None


def find_harmonia_binary(
    binary_path: Optional[Union[str, os.PathLike[str]]] = None,
) -> Optional[Path]:
    """Locate an executable Harmonia pure-OM-2 native binary, or return None."""
    if binary_path is not None:
        p = Path(binary_path)
        return p if p.is_file() and os.access(p, os.X_OK) else None

    env_override = os.environ.get("HARMONIA_OMEGA_BIN")
    if env_override is not None:
        if env_override == "":
            return None
        p = Path(env_override)
        return p if p.is_file() and os.access(p, os.X_OK) else None

    bin_name = _platform_binary_name()
    if bin_name is None:
        return None

    here = Path(__file__).resolve()
    candidates = [
        here.parent / "bin" / bin_name,
        here.parent.parent / "bin" / bin_name,
        Path.cwd() / "bin" / bin_name,
        Path.home() / "workspace" / "omega-harmonia" / "bin" / bin_name,
    ]
    for cand in candidates:
        if cand.is_file() and os.access(cand, os.X_OK):
            return cand

    which_hit = shutil.which(bin_name) or shutil.which("harmonia-om")
    if which_hit:
        p = Path(which_hit)
        if p.is_file() and os.access(p, os.X_OK):
            return p
    return None


def _norm_zero(x: float) -> float:
    return 0.0 if x == 0.0 else float(x)


def _f64_hex(x: float) -> str:
    return f"0x{struct.unpack('>Q', struct.pack('>d', _norm_zero(x)))[0]:016x}"


def _fmt_f64(x: float) -> str:
    return repr(_norm_zero(x))


def _make_receipt(op: str, in_str: str, out_str: str, status: int) -> tuple[str, str]:
    preimage = f"HARMONIA-OM2-RECEIPT-V1|op={op}|in={in_str}|out={out_str}|status={status}"
    digest = hashlib.sha256(preimage.encode("utf-8")).hexdigest()
    return preimage, digest


def _verify_native_json(payload: dict[str, Any]) -> None:
    pre = payload.get("receipt_preimage", "")
    got = payload.get("sha256", "")
    expected = hashlib.sha256(pre.encode("utf-8")).hexdigest()
    if not got or got != expected:
        raise OmegaReceiptTamperError(
            f"Native receipt SHA-256 mismatch: expected={expected} got={got}"
        )


def _run_native(
    args: list[str],
    binary_path: Optional[Union[str, os.PathLike[str]]] = None,
) -> Optional[tuple[int, dict[str, Any]]]:
    exe = find_harmonia_binary(binary_path)
    if exe is None:
        return None
    proc = subprocess.run(
        [str(exe), *args],
        capture_output=True,
        text=True,
        check=False,
        timeout=5.0,
    )
    out = proc.stdout.strip()
    if not out:
        raise RuntimeError(
            f"Native binary {exe} exited {proc.returncode} with empty stdout; stderr={proc.stderr.strip()}"
        )
    data = json.loads(out)
    _verify_native_json(data)
    return proc.returncode, data


def _cabs(z: complex) -> float:
    return math.hypot(z.real, z.imag)


class HarmoniaOmegaBridge:
    """Bridge dispatching Harmonia math and governance checks to OM-2 or fallback."""

    def __init__(
        self,
        binary_path: Optional[Union[str, os.PathLike[str]]] = None,
        prefer_native: bool = True,
    ):
        self.binary_path = Path(binary_path) if binary_path is not None else None
        self.prefer_native = prefer_native

    @property
    def native_available(self) -> bool:
        return self.prefer_native and find_harmonia_binary(self.binary_path) is not None

    def _call_native(self, args: list[str]) -> Optional[tuple[int, dict[str, Any]]]:
        if not self.prefer_native:
            return None
        return _run_native(args, self.binary_path)

    def eval_operator(
        self,
        op: str,
        z: complex = 0j,
        w: complex = 0j,
        n: int = 1,
    ) -> OmegaReceiptResult:
        z = complex(z)
        w = complex(w)
        canonical_ops = {
            "Φ": "Phi", "Phi": "Phi",
            "π": "Pi", "Pi": "Pi",
            "ε": "Eps", "Eps": "Eps",
            "Λ": "Lam", "Lam": "Lam",
            "Δ": "Del", "Del": "Del",
            "Ψ": "Psi", "Psi": "Psi",
            "Ω": "Omega", "Omega": "Omega",
        }
        tag = canonical_ops.get(op)
        if tag is None:
            raise ValueError(f"Unknown Harmonia math operator: {op!r}")

        if tag == "Omega":
            args = ["--op", "Omega", _fmt_f64(z.real), _fmt_f64(z.imag), _fmt_f64(w.real), _fmt_f64(w.imag)]
        elif tag == "Pi":
            args = ["--op", "Pi", _fmt_f64(z.real), _fmt_f64(z.imag), _fmt_f64(w.real), _fmt_f64(w.imag), str(int(n))]
        else:
            args = ["--op", tag, _fmt_f64(z.real), _fmt_f64(z.imag), _fmt_f64(w.real), _fmt_f64(w.imag)]

        native = self._call_native(args)
        if native is not None:
            rc, d = native
            val = None
            if d["ok"] and d["real"] is not None:
                val = complex(float(d["real"]), float(d["imag"]))
            return OmegaReceiptResult(
                ok=bool(d["ok"]),
                op=str(d["op"]),
                status=int(d["status"]),
                verdict=str(d["verdict"]),
                reason=str(d["reason"]),
                value=val,
                sha256=str(d["sha256"]),
                receipt_preimage=str(d["receipt_preimage"]),
                backend="omega-om2-native",
                exit_code=rc,
                real_bits=d.get("real_bits"),
                imag_bits=d.get("imag_bits"),
                abs_value=d.get("abs"),
            )

        # Fallback to authoritative phi_pi_e_math_core.py
        core = _core()
        in_base = f"{_fmt_f64(z.real)},{_fmt_f64(z.imag)},{_fmt_f64(w.real)},{_fmt_f64(w.imag)}"
        if tag == "Omega":
            if not (math.isfinite(z.real) and math.isfinite(z.imag) and math.isfinite(w.real) and math.isfinite(w.imag)):
                pre, sha = _make_receipt("CLI", "invalid_float", "REFUSED:invalid_arguments", STATUS_CLI_ERROR)
                return OmegaReceiptResult(
                    ok=False, op="CLI", status=STATUS_CLI_ERROR, verdict="REFUSED",
                    reason="invalid_arguments", value=None, sha256=sha, receipt_preimage=pre,
                    backend="python-fallback", exit_code=1,
                )
            rsn = "omega_theorem_3_2_categorical_boundary"
            pre, sha = _make_receipt("Omega", in_base, f"REFUSED:{rsn}", STATUS_OMEGA_BOUNDARY)
            return OmegaReceiptResult(
                ok=False, op="Omega", status=STATUS_OMEGA_BOUNDARY, verdict="REFUSED",
                reason=rsn, value=None, sha256=sha, receipt_preimage=pre,
                backend="python-fallback", exit_code=11,
            )

        if not (math.isfinite(z.real) and math.isfinite(z.imag) and math.isfinite(w.real) and math.isfinite(w.imag)):
            pre, sha = _make_receipt("CLI", "invalid_float", "REFUSED:invalid_arguments", STATUS_CLI_ERROR)
            return OmegaReceiptResult(
                ok=False, op="CLI", status=STATUS_CLI_ERROR, verdict="REFUSED",
                reason="invalid_arguments", value=None, sha256=sha, receipt_preimage=pre,
                backend="python-fallback", exit_code=1,
            )

        if tag == "Pi":
            in_str = f"{in_base},{int(n)}"
            if w == 0:
                rsn = "pi_w_zero_undefined_thm_3_2"
                pre, sha = _make_receipt("Pi", in_str, f"REFUSED:{rsn}", STATUS_PI_W_ZERO)
                return OmegaReceiptResult(
                    ok=False, op="Pi", status=STATUS_PI_W_ZERO, verdict="REFUSED",
                    reason=rsn, value=None, sha256=sha, receipt_preimage=pre,
                    backend="python-fallback", exit_code=12,
                )
            if int(n) < 1:
                rsn = "pi_depth_lt_1"
                pre, sha = _make_receipt("Pi", in_str, f"REFUSED:{rsn}", STATUS_PI_DEPTH_LT1)
                return OmegaReceiptResult(
                    ok=False, op="Pi", status=STATUS_PI_DEPTH_LT1, verdict="REFUSED",
                    reason=rsn, value=None, sha256=sha, receipt_preimage=pre,
                    backend="python-fallback", exit_code=13,
                )
            res = core.transcendent_continuity(z, w, n=int(n))
        else:
            in_str = in_base
            fn = {
                "Phi": core.harmonic_equilibrium,
                "Eps": core.incremental_insight,
                "Lam": core.structural_illumination,
                "Del": core.fusion_transformation,
                "Psi": core.recursive_animation,
            }[tag]
            res = fn(z, w)

        rr = _norm_zero(res.real)
        ri = _norm_zero(res.imag)
        norm_c = complex(rr, ri)
        ab = _cabs(norm_c)
        if not (math.isfinite(rr) and math.isfinite(ri) and math.isfinite(ab)):
            in_final = f"{in_base},{int(n)}" if tag == "Pi" else in_base
            pre, sha = _make_receipt(tag, in_final, "REFUSED:non_finite_overflow", STATUS_OVERFLOW)
            return OmegaReceiptResult(
                ok=False, op=tag, status=STATUS_OVERFLOW, verdict="REFUSED",
                reason="non_finite_overflow", value=None, sha256=sha, receipt_preimage=pre,
                backend="python-fallback", exit_code=19,
            )
        pre, sha = _make_receipt(tag, in_str, f"{_fmt_f64(rr)},{_fmt_f64(ri)},{_fmt_f64(ab)}", STATUS_OK)
        return OmegaReceiptResult(
            ok=True, op=tag, status=STATUS_OK, verdict="OK", reason="ok",
            value=norm_c, sha256=sha, receipt_preimage=pre, backend="python-fallback",
            exit_code=0, real_bits=_f64_hex(rr), imag_bits=_f64_hex(ri), abs_value=ab,
        )

    def eval_corridor(self, phi: float, psi: float, eps: float) -> OmegaReceiptResult:
        p_val, s_val, e_val = float(phi), float(psi), float(eps)
        native = self._call_native(["--corridor", _fmt_f64(p_val), _fmt_f64(s_val), _fmt_f64(e_val)])
        if native is not None:
            rc, d = native
            val = float(d["sigma"]) if d.get("ok") and d.get("sigma") is not None else None
            return OmegaReceiptResult(
                ok=bool(d["ok"]), op=str(d["op"]), status=int(d["status"]),
                verdict=str(d["verdict"]), reason=str(d["reason"]),
                value=val, sha256=str(d["sha256"]),
                receipt_preimage=str(d["receipt_preimage"]),
                backend="omega-om2-native", exit_code=rc,
                sigma_bits=d.get("sigma_bits"),
            )

        if not (math.isfinite(p_val) and math.isfinite(s_val) and math.isfinite(e_val)):
            pre, sha = _make_receipt("CLI", "invalid_float", "REFUSED:invalid_arguments", STATUS_CLI_ERROR)
            return OmegaReceiptResult(
                ok=False, op="CLI", status=STATUS_CLI_ERROR, verdict="REFUSED",
                reason="invalid_arguments", value=None, sha256=sha, receipt_preimage=pre,
                backend="python-fallback", exit_code=1,
            )
        sig = _norm_zero((s_val + p_val) * (1.0 - e_val))
        in_str = f"{_fmt_f64(p_val)},{_fmt_f64(s_val)},{_fmt_f64(e_val)}"
        if not math.isfinite(sig):
            pre, sha = _make_receipt("Sigma", in_str, "REFUSED:non_finite_overflow", STATUS_OVERFLOW)
            return OmegaReceiptResult(
                ok=False, op="Sigma", status=STATUS_OVERFLOW, verdict="REFUSED",
                reason="non_finite_overflow", value=None, sha256=sha, receipt_preimage=pre,
                backend="python-fallback", exit_code=19,
            )
        pre, sha = _make_receipt("Sigma", in_str, _fmt_f64(sig), STATUS_OK)
        return OmegaReceiptResult(
            ok=True, op="Sigma", status=STATUS_OK, verdict="OK", reason="ok",
            value=sig, sha256=sha, receipt_preimage=pre, backend="python-fallback",
            exit_code=0, sigma_bits=_f64_hex(sig),
        )

    def check_pipe_disjoint(self, mask_a: int, mask_b: int) -> OmegaReceiptResult:
        ma, mb = int(mask_a), int(mask_b)
        if ma < 0 or mb < 0:
            raise ValueError("Sector bitmasks must be non-negative")
        native = self._call_native(["--guard", "pipe", str(ma), str(mb)])
        if native is not None:
            rc, d = native
            return OmegaReceiptResult(
                ok=bool(d["ok"]), op=str(d["op"]), status=int(d["status"]),
                verdict=str(d["verdict"]), reason=str(d["reason"]),
                value=None, sha256=str(d["sha256"]),
                receipt_preimage=str(d["receipt_preimage"]),
                backend="omega-om2-native", exit_code=rc,
            )
        ok = (ma != 0) and (mb != 0) and ((ma & mb) == 0)
        st = STATUS_OK if ok else STATUS_GOV_PIPE_OVERLAP
        rsn = "ok" if ok else "gov_pipe_sector_not_disjoint"
        out_str = "PASS" if ok else f"REFUSED:{rsn}"
        pre, sha = _make_receipt("GovPipe", f"{ma},{mb}", out_str, st)
        return OmegaReceiptResult(
            ok=ok, op="GovPipe", status=st, verdict="OK" if ok else "REFUSED",
            reason=rsn, value=None, sha256=sha, receipt_preimage=pre,
            backend="python-fallback", exit_code=0 if ok else 14,
        )

    def check_bracket_depth(self, depth: int, ceiling: int) -> OmegaReceiptResult:
        dp, cl = int(depth), int(ceiling)
        native = self._call_native(["--guard", "bracket", str(dp), str(cl)])
        if native is not None:
            rc, d = native
            return OmegaReceiptResult(
                ok=bool(d["ok"]), op=str(d["op"]), status=int(d["status"]),
                verdict=str(d["verdict"]), reason=str(d["reason"]),
                value=None, sha256=str(d["sha256"]),
                receipt_preimage=str(d["receipt_preimage"]),
                backend="omega-om2-native", exit_code=rc,
            )
        ok = (cl >= 1) and (0 <= dp <= cl)
        st = STATUS_OK if ok else STATUS_GOV_BRACKET_DEPTH
        rsn = "ok" if ok else "gov_bracket_depth_exceeded"
        out_str = "PASS" if ok else f"REFUSED:{rsn}"
        pre, sha = _make_receipt("GovBracket", f"{dp},{cl}", out_str, st)
        return OmegaReceiptResult(
            ok=ok, op="GovBracket", status=st, verdict="OK" if ok else "REFUSED",
            reason=rsn, value=None, sha256=sha, receipt_preimage=pre,
            backend="python-fallback", exit_code=0 if ok else 15,
        )

    def check_arrow_acyclic(self, states: Sequence[Any]) -> OmegaReceiptResult:
        items = [str(s) for s in states]
        for item in items:
            try:
                raw_b = item.encode("utf-8", errors="strict")
            except UnicodeEncodeError:
                raw_b = b"\x00"
            if any(b < 32 for b in raw_b) or len(raw_b) > 1024:
                pre, sha = _make_receipt("CLI", "oversized_or_invalid_frame", "REFUSED:invalid_arguments", STATUS_CLI_ERROR)
                return OmegaReceiptResult(
                    ok=False, op="CLI", status=STATUS_CLI_ERROR, verdict="REFUSED",
                    reason="invalid_arguments", value=None, sha256=sha, receipt_preimage=pre,
                    backend="omega-om2-native" if self.native_available else "python-fallback",
                    exit_code=1,
                )
        if len(items) > 256 or sum(len(s.encode("utf-8")) + 1 for s in items) > 7680:
            pre, sha = _make_receipt("CLI", "oversized_or_invalid_frame", "REFUSED:invalid_arguments", STATUS_CLI_ERROR)
            return OmegaReceiptResult(
                ok=False, op="CLI", status=STATUS_CLI_ERROR, verdict="REFUSED",
                reason="invalid_arguments", value=None, sha256=sha, receipt_preimage=pre,
                backend="omega-om2-native" if self.native_available else "python-fallback",
                exit_code=1,
            )
        if len(items) < 2:
            st = STATUS_GOV_ARROW_CYCLE
            rsn = "gov_arrow_cycle_detected"
            pre, sha = _make_receipt("GovArrow", ",".join(items), f"REFUSED:{rsn}", st)
            return OmegaReceiptResult(
                ok=False, op="GovArrow", status=st, verdict="REFUSED",
                reason=rsn, value=None, sha256=sha, receipt_preimage=pre,
                backend="omega-om2-native" if self.native_available else "python-fallback",
                exit_code=16,
            )
        native = self._call_native(["--guard", "arrow", *items])
        if native is not None:
            rc, d = native
            return OmegaReceiptResult(
                ok=bool(d["ok"]), op=str(d["op"]), status=int(d["status"]),
                verdict=str(d["verdict"]), reason=str(d["reason"]),
                value=None, sha256=str(d["sha256"]),
                receipt_preimage=str(d["receipt_preimage"]),
                backend="omega-om2-native", exit_code=rc,
            )
        seen: set[tuple[str, Any]] = set()
        ok = True
        for raw in items:
            try:
                num = float(raw)
                if math.isfinite(num):
                    key = ("f", _norm_zero(num))
                else:
                    key = ("s", raw)
            except ValueError:
                key = ("s", raw)
            if key in seen:
                ok = False
                break
            seen.add(key)
        st = STATUS_OK if ok else STATUS_GOV_ARROW_CYCLE
        rsn = "ok" if ok else "gov_arrow_cycle_detected"
        out_str = "PASS" if ok else f"REFUSED:{rsn}"
        pre, sha = _make_receipt("GovArrow", ",".join(items), out_str, st)
        return OmegaReceiptResult(
            ok=ok, op="GovArrow", status=st, verdict="OK" if ok else "REFUSED",
            reason=rsn, value=None, sha256=sha, receipt_preimage=pre,
            backend="python-fallback", exit_code=0 if ok else 16,
        )

    def check_eq_lock(self, locked_val: float, proposed_val: float, lock_flag: int = 1) -> OmegaReceiptResult:
        lv, pv, fg = float(locked_val), float(proposed_val), int(lock_flag)
        native = self._call_native(["--guard", "eq", _fmt_f64(lv), _fmt_f64(pv), str(fg)])
        if native is not None:
            rc, d = native
            return OmegaReceiptResult(
                ok=bool(d["ok"]), op=str(d["op"]), status=int(d["status"]),
                verdict=str(d["verdict"]), reason=str(d["reason"]),
                value=None, sha256=str(d["sha256"]),
                receipt_preimage=str(d["receipt_preimage"]),
                backend="omega-om2-native", exit_code=rc,
            )
        ok = (fg == 1) and math.isfinite(lv) and math.isfinite(pv) and (lv == pv)
        st = STATUS_OK if ok else STATUS_GOV_EQ_LOCK
        rsn = "ok" if ok else "gov_eq_lock_violation"
        out_str = "PASS" if ok else f"REFUSED:{rsn}"
        pre, sha = _make_receipt("GovEq", f"{_fmt_f64(lv)},{_fmt_f64(pv)},{fg}", out_str, st)
        return OmegaReceiptResult(
            ok=ok, op="GovEq", status=st, verdict="OK" if ok else "REFUSED",
            reason=rsn, value=None, sha256=sha, receipt_preimage=pre,
            backend="python-fallback", exit_code=0 if ok else 17,
        )

    def verify_receipt(self, preimage: str, sha256_hex: str) -> bool:
        try:
            pre_bytes = preimage.encode("utf-8", errors="strict")
            sha_bytes = sha256_hex.encode("utf-8", errors="strict")
        except UnicodeEncodeError:
            return False
        if "\x00" in preimage or "\x00" in sha256_hex or len(pre_bytes) > 8192 or len(sha_bytes) > 256:
            return False
        expected = hashlib.sha256(pre_bytes).hexdigest()
        native_ok = True
        exe = find_harmonia_binary(self.binary_path) if self.prefer_native else None
        if exe is not None:
            proc = subprocess.run(
                [str(exe), "--verify-receipt", preimage, sha256_hex],
                capture_output=True, text=True, check=False, timeout=5.0,
            )
            d = json.loads(proc.stdout.strip())
            native_ok = (proc.returncode == 0 and bool(d.get("ok")))
        return native_ok and (sha256_hex.lower() == expected)


# ===== Drop-in math-core compatible functional helpers =====

_DEFAULT_BRIDGE = HarmoniaOmegaBridge()


def harmonic_equilibrium(z: complex, w: complex) -> complex:
    res = _DEFAULT_BRIDGE.eval_operator("Phi", z, w)
    return res.value  # type: ignore[return-value]


def transcendent_continuity(z: complex, w: complex, n: int = 1) -> complex:
    res = _DEFAULT_BRIDGE.eval_operator("Pi", z, w, n=n)
    if not res.ok:
        if res.status == STATUS_PI_W_ZERO:
            raise ValueError("π(z,w) undefined for w = 0 (proofs, Thm 3.2)")
        raise ValueError("recursion depth n must be a positive integer")
    return res.value  # type: ignore[return-value]


def incremental_insight(z: complex, w: complex) -> complex:
    res = _DEFAULT_BRIDGE.eval_operator("Eps", z, w)
    return res.value  # type: ignore[return-value]


def structural_illumination(z: complex, w: complex) -> complex:
    res = _DEFAULT_BRIDGE.eval_operator("Lam", z, w)
    return res.value  # type: ignore[return-value]


def fusion_transformation(z: complex, w: complex) -> complex:
    res = _DEFAULT_BRIDGE.eval_operator("Del", z, w)
    return res.value  # type: ignore[return-value]


def recursive_animation(z: complex, w: complex) -> complex:
    res = _DEFAULT_BRIDGE.eval_operator("Psi", z, w)
    return res.value  # type: ignore[return-value]


def scalar_corridor(phi: float, psi: float, eps: float) -> float:
    res = _DEFAULT_BRIDGE.eval_corridor(phi, psi, eps)
    return float(res.value)  # type: ignore[arg-type]


def categorical_omega(z: complex = 0j, w: complex = 0j) -> None:
    res = _DEFAULT_BRIDGE.eval_operator("Omega", z, w)
    try:
        core = _core()
        core.CATEGORICAL_OPERATORS["Ω"](z, w)
    except ImportError:
        pass
    raise OmegaBoundaryRefusal(
        f"Ω (Qualia Gateway) refused numerically (status {res.status})",
        status=res.status,
        receipt=res,
    )
