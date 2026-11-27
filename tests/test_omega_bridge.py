# Tests for harmonia_omega_bridge.py (PR 4)
#
# Runs completely in CI without native binaries (via python-fallback) AND
# verifies live native parity + identical SHA-256 receipts when a compiled
# pure seeded-OM-2 binary (`harmonia-om-macos` / `harmonia-om-linux`) is
# available (or when HARMONIA_REQUIRE_OMEGA=1).

import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

import harmonia_omega_bridge as ob
from harmonia_omega_bridge import (
    HarmoniaOmegaBridge,
    OmegaBoundaryRefusal,
    OmegaReceiptTamperError,
    STATUS_GOV_ARROW_CYCLE,
    STATUS_GOV_BRACKET_DEPTH,
    STATUS_GOV_EQ_LOCK,
    STATUS_GOV_PIPE_OVERLAP,
    STATUS_OK,
    STATUS_OMEGA_BOUNDARY,
    STATUS_PI_DEPTH_LT1,
    STATUS_PI_W_ZERO,
    categorical_omega,
    find_harmonia_binary,
    fusion_transformation,
    harmonic_equilibrium,
    incremental_insight,
    recursive_animation,
    scalar_corridor,
    structural_illumination,
    transcendent_continuity,
)
from phi_pi_e_math_core import (
    CATEGORICAL_OPERATORS,
    CategoricalBoundaryError,
    fusion_transformation as py_delta,
    harmonic_equilibrium as py_phi,
    incremental_insight as py_eps,
    recursive_animation as py_psi,
    structural_illumination as py_lam,
    transcendent_continuity as py_pi,
)

SAMPLES = [
    (3 + 4j, 1 - 2j),
    (2 + 3j, 1 + 1j),
    (-1 - 1j, 4 + 0.5j),
    (5 + 0j, 5 + 0j),
]


class TestFallbackAndParity:
    def test_explicit_fallback_matches_math_core(self):
        bridge = HarmoniaOmegaBridge(prefer_native=False)
        assert not bridge.native_available
        for z, w in SAMPLES:
            checks = [
                ("Φ", py_phi(z, w)),
                ("ε", py_eps(z, w)),
                ("Λ", py_lam(z, w)),
                ("Δ", py_delta(z, w)),
                ("Ψ", py_psi(z, w)),
            ]
            for sym, expected in checks:
                res = bridge.eval_operator(sym, z, w)
                assert res.ok and res.status == STATUS_OK
                assert res.backend == "python-fallback"
                assert abs(res.value - expected) < 1e-12
                assert bridge.verify_receipt(res.receipt_preimage, res.sha256)

            pi_res = bridge.eval_operator("π", z, w, n=4)
            assert pi_res.ok and abs(pi_res.value - py_pi(z, w, n=4)) < 1e-12

    def test_env_disable_forces_fallback(self, monkeypatch):
        monkeypatch.setenv("HARMONIA_OMEGA_BIN", "")
        assert find_harmonia_binary() is None
        bridge = HarmoniaOmegaBridge()
        assert not bridge.native_available
        res = bridge.eval_corridor(5.0, 3.0, 0.2)
        assert res.backend == "python-fallback"
        assert abs(res.value - 6.4) < 1e-12
        assert res.sha256 == hashlib.sha256(res.receipt_preimage.encode("utf-8")).hexdigest()

    def test_drop_in_functional_helpers_with_fallback(self, monkeypatch):
        monkeypatch.setattr(ob, "_DEFAULT_BRIDGE", HarmoniaOmegaBridge(prefer_native=False))
        z, w = 3 + 4j, 1 - 2j
        assert abs(harmonic_equilibrium(z, w) - py_phi(z, w)) < 1e-12
        assert abs(transcendent_continuity(z, w, n=4) - py_pi(z, w, n=4)) < 1e-12
        assert abs(incremental_insight(z, w) - py_eps(z, w)) < 1e-12
        assert abs(structural_illumination(z, w) - py_lam(z, w)) < 1e-12
        assert abs(fusion_transformation(z, w) - py_delta(z, w)) < 1e-12
        assert abs(recursive_animation(z, w) - py_psi(z, w)) < 1e-12
        assert abs(scalar_corridor(5.0, 3.0, 0.2) - 6.4) < 1e-12

        with pytest.raises(ValueError):
            transcendent_continuity(1 + 1j, 0)
        with pytest.raises((CategoricalBoundaryError, OmegaBoundaryRefusal)):
            categorical_omega(1 + 1j, 2 - 1j)


class TestRefusalsAndGovernance:
    def test_omega_refusal_and_pi_domain_refusals(self):
        bridge = HarmoniaOmegaBridge(prefer_native=False)
        omega = bridge.eval_operator("Ω", 1 + 1j, 2 - 1j)
        assert not omega.ok
        assert omega.status == STATUS_OMEGA_BOUNDARY
        assert omega.verdict == "REFUSED"
        assert omega.value is None
        assert bridge.verify_receipt(omega.receipt_preimage, omega.sha256)

        pi_zero = bridge.eval_operator("π", 1 + 1j, 0j, n=4)
        assert not pi_zero.ok and pi_zero.status == STATUS_PI_W_ZERO

        pi_bad_n = bridge.eval_operator("π", 1 + 1j, 2 + 0j, n=0)
        assert not pi_bad_n.ok and pi_bad_n.status == STATUS_PI_DEPTH_LT1

    def test_governance_guards_pass_and_refuse(self):
        bridge = HarmoniaOmegaBridge(prefer_native=False)

        assert bridge.check_pipe_disjoint(0b01, 0b10).ok
        bad_pipe = bridge.check_pipe_disjoint(0b11, 0b10)
        assert not bad_pipe.ok and bad_pipe.status == STATUS_GOV_PIPE_OVERLAP

        assert bridge.check_bracket_depth(4, 10).ok
        bad_bracket = bridge.check_bracket_depth(11, 10)
        assert not bad_bracket.ok and bad_bracket.status == STATUS_GOV_BRACKET_DEPTH

        assert bridge.check_arrow_acyclic(["s0", "s1", "s2"]).ok
        bad_arrow = bridge.check_arrow_acyclic(["1", "2", "1"])
        assert not bad_arrow.ok and bad_arrow.status == STATUS_GOV_ARROW_CYCLE

        assert bridge.check_eq_lock(6.4, 6.4, 1).ok
        bad_lock = bridge.check_eq_lock(6.4, 7.0, 1)
        assert not bad_lock.ok and bad_lock.status == STATUS_GOV_EQ_LOCK

    def test_receipt_tamper_detection(self):
        bridge = HarmoniaOmegaBridge(prefer_native=False)
        res = bridge.eval_corridor(5.0, 3.0, 0.2)
        assert bridge.verify_receipt(res.receipt_preimage, res.sha256)
        tampered_hex = ("0" if res.sha256[0] != "0" else "1") + res.sha256[1:]
        assert not bridge.verify_receipt(res.receipt_preimage, tampered_hex)

        with pytest.raises(OmegaReceiptTamperError):
            ob._verify_native_json({
                "receipt_preimage": res.receipt_preimage,
                "sha256": tampered_hex,
            })

    def test_math_core_categorical_omega_untouched(self):
        with pytest.raises(CategoricalBoundaryError):
            CATEGORICAL_OPERATORS["Ω"](1 + 1j, 2 - 1j)


_NATIVE_BIN = find_harmonia_binary()
_REQUIRE_NATIVE = os.environ.get("HARMONIA_REQUIRE_OMEGA") == "1"


@pytest.mark.skipif(
    _NATIVE_BIN is None and not _REQUIRE_NATIVE,
    reason="Native harmonia-om binary not present (set HARMONIA_REQUIRE_OMEGA=1 to enforce)",
)
class TestLiveNativeOmegaParity:
    def test_native_binary_matches_fallback_and_receipts(self):
        assert _NATIVE_BIN is not None, "HARMONIA_REQUIRE_OMEGA=1 but binary not found"
        native = HarmoniaOmegaBridge(binary_path=_NATIVE_BIN, prefer_native=True)
        fallback = HarmoniaOmegaBridge(prefer_native=False)

        corridor_n = native.eval_corridor(5.0, 3.0, 0.2)
        corridor_f = fallback.eval_corridor(5.0, 3.0, 0.2)
        assert corridor_n.backend == "omega-om2-native"
        assert corridor_n.value == 6.4
        assert corridor_n.sha256 == corridor_f.sha256
        assert native.verify_receipt(corridor_n.receipt_preimage, corridor_n.sha256)

        for sym in ("Φ", "π", "ε", "Λ", "Δ", "Ψ"):
            rn = native.eval_operator(sym, 3 + 4j, 1 - 2j, n=4)
            rf = fallback.eval_operator(sym, 3 + 4j, 1 - 2j, n=4)
            assert rn.ok and rn.backend == "omega-om2-native"
            assert abs(rn.value - rf.value) <= 1e-12
            assert native.verify_receipt(rn.receipt_preimage, rn.sha256)
            assert rn.sha256 == hashlib.sha256(rn.receipt_preimage.encode("utf-8")).hexdigest()

        om_n = native.eval_operator("Ω", 1 + 1j, 2 - 1j)
        om_f = fallback.eval_operator("Ω", 1 + 1j, 2 - 1j)
        assert not om_n.ok and om_n.status == STATUS_OMEGA_BOUNDARY
        assert om_n.sha256 == om_f.sha256

        pi0_n = native.eval_operator("π", 1 + 1j, 0j, n=4)
        assert not pi0_n.ok and pi0_n.status == STATUS_PI_W_ZERO

        assert not native.verify_receipt(
            corridor_n.receipt_preimage,
            ("0" if corridor_n.sha256[0] != "0" else "1") + corridor_n.sha256[1:],
        )
