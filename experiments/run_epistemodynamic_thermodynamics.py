#!/usr/bin/env python3
"""Run the RI1 Epistemodynamics thermodynamic policy comparison.

Example:
    python3 -m experiments.run_epistemodynamic_thermodynamics \
        --output-dir /tmp/epistemodynamics-run

The runner writes JSON and CSV traces.  It never overwrites repository source
files and it uses no external service or model API.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable

from .epistemodynamic_thermodynamics import (
    AdaptivePhi,
    FixedPhi,
    NoMediation,
    ThermoParameters,
    closed_system_conservation_audit,
    energy_accounting_error,
    result_as_dict,
    run_open_system,
    structural_energy,
)


def _format(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def write_trace_csv(path: Path, results: Iterable) -> None:
    fieldnames = [
        "policy", "step", "entropy", "coherence", "reservoir", "phi",
        "entropy_produced", "entropy_reduced", "phase", "collapsed",
        "energy_accounting_error",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            for state in result.trace:
                writer.writerow({
                    "policy": result.policy,
                    "step": state.step,
                    "entropy": state.entropy,
                    "coherence": state.coherence,
                    "reservoir": state.reservoir,
                    "phi": state.phi,
                    "entropy_produced": state.entropy_produced,
                    "entropy_reduced": state.entropy_reduced,
                    "phase": state.phase.value,
                    "collapsed": state.collapsed,
                    "energy_accounting_error": energy_accounting_error(
                        state, result.parameters
                    ),
                })


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path, required=True,
        help="New or existing directory for JSON and CSV experiment outputs.",
    )
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--integration-rate", type=float, default=0.70)
    parser.add_argument("--requested-reduction", type=float, default=0.040)
    args = parser.parse_args()

    parameters = ThermoParameters(
        steps=args.steps,
        integration_rate=args.integration_rate,
        requested_entropy_reduction=args.requested_reduction,
    )
    policies = (NoMediation(), FixedPhi(), AdaptivePhi())
    results = [run_open_system(policy, parameters) for policy in policies]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "policy_comparison.json"
    csv_path = args.output_dir / "policy_trace.csv"
    audit_path = args.output_dir / "closed_system_audit.json"

    json_path.write_text(
        json.dumps([result_as_dict(result) for result in results], indent=2),
        encoding="utf-8",
    )
    write_trace_csv(csv_path, results)

    audit = closed_system_conservation_audit(
        mass=parameters.mass,
        # This is a strictly closed Law-2 audit, so its total must equal
        # the initial two-term structural energy. The open-system experiment
        # above deliberately uses the larger declared budget E_total, whose
        # residual is represented by the extension reservoir D.
        total_energy=structural_energy(
            parameters.mass,
            parameters.initial_entropy,
            parameters.initial_coherence,
        ),
        entropy_before=parameters.initial_entropy,
        entropy_after=parameters.initial_entropy + 0.10,
        coherence_before=parameters.initial_coherence,
    )
    audit_path.write_text(
        json.dumps({
            "question": (
                "If m and E=m(1-S)+C^2 are fixed in a closed system, "
                "what coherence follows from a +0.10 entropy change?"
            ),
            "result": {
                "mass": audit.mass,
                "total_energy": audit.total_energy,
                "entropy_before": audit.entropy_before,
                "entropy_after": audit.entropy_after,
                "coherence_before": audit.coherence_before,
                "coherence_required_after": audit.coherence_required_after,
                "coherence_delta_required": audit.coherence_delta_required,
                "feasible": audit.feasible,
            },
        }, indent=2),
        encoding="utf-8",
    )

    print("RI1 Epistemodynamics thermodynamic policy comparison")
    print("Model status: deterministic toy model; parameters are declared, not fitted.")
    print()
    print(
        f"{'policy':<16} {'collapse':>9} {'S_final':>10} {'C_final':>10} "
        f"{'D_final':>10} {'phase':>10}"
    )
    print("-" * 74)
    for result in results:
        summary = result.summary()
        print(
            f"{summary['policy']:<16} "
            f"{_format(summary['collapse_step'] if summary['collapse_step'] is not None else 'none'):>9} "
            f"{_format(summary['final_entropy']):>10} "
            f"{_format(summary['final_coherence']):>10} "
            f"{_format(summary['final_reservoir']):>10} "
            f"{summary['final_phase']:>10}"
        )
    print()
    print("Closed-system Law-2 audit (+0.10 entropy):")
    print(f"  coherence before:         {_format(audit.coherence_before)}")
    print(f"  coherence required after: {_format(audit.coherence_required_after)}")
    print(f"  required coherence delta: {_format(audit.coherence_delta_required)}")
    print()
    print(f"Wrote {json_path}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {audit_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
