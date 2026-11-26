#!/usr/bin/env python3
"""Map declared thermodynamic-policy outcomes across a parameter grid.

Example:
    python3 -m experiments.sweep_epistemodynamic_thermodynamics \
        --output-csv /tmp/epistemodynamics-sweep.csv

The result is a deterministic sensitivity map, not an empirical validation.
It answers where this explicitly declared model crosses its own Law-6/Law-20
collapse boundary under different integration pressure and requested Φ-mediated
entropy-reduction rates.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .epistemodynamic_thermodynamics import (
    AdaptivePhi,
    FixedPhi,
    NoMediation,
    ThermoParameters,
    run_open_system,
)


DEFAULT_INTEGRATION_RATES = (0.30, 0.50, 0.70, 0.90, 1.10)
DEFAULT_REDUCTION_RATES = (0.020, 0.040, 0.060, 0.080, 0.100)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument(
        "--integration-rates", type=float, nargs="+", default=DEFAULT_INTEGRATION_RATES,
    )
    parser.add_argument(
        "--reduction-rates", type=float, nargs="+", default=DEFAULT_REDUCTION_RATES,
    )
    args = parser.parse_args()

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    policies = (NoMediation(), FixedPhi(), AdaptivePhi())
    rows = []
    for integration_rate in args.integration_rates:
        for requested_reduction in args.reduction_rates:
            parameters = ThermoParameters(
                steps=args.steps,
                integration_rate=integration_rate,
                requested_entropy_reduction=requested_reduction,
            )
            for policy in policies:
                result = run_open_system(policy, parameters)
                summary = result.summary()
                rows.append({
                    "policy": summary["policy"],
                    "integration_rate": integration_rate,
                    "requested_entropy_reduction": requested_reduction,
                    "collapse_step": summary["collapse_step"],
                    "final_phase": summary["final_phase"],
                    "final_entropy": summary["final_entropy"],
                    "final_coherence": summary["final_coherence"],
                    "minimum_reservoir": summary["min_reservoir"],
                })

    fields = list(rows[0])
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {args.output_csv} ({len(rows)} policy conditions)")
    for policy in policies:
        policy_rows = [row for row in rows if row["policy"] == policy.name]
        survived = sum(row["collapse_step"] is None for row in policy_rows)
        print(f"{policy.name}: {survived}/{len(policy_rows)} conditions survive {args.steps} steps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
