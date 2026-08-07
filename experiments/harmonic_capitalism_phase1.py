"""Harmonic Capitalism Phase 1 — comparative run (ECONOMY_SIM_PHASE1.md).

Runs both worlds on the same seed with the same guard and prints the
comparison, including governance's COST (which is not zero, and is
reported as a headline number).

Usage:  python3 -m experiments.harmonic_capitalism_phase1
"""

import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm_brain.economy import FLOOR, SHOCK_MAG, SHOCK_ROUNDS, STRESS, run_pair


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        tp, bd = run_pair()

    print("=" * 72)
    print("HARMONIC CAPITALISM — PHASE 1: the naive-guard experiment")
    print("=" * 72)
    print(f"Identical agents, identical seed, identical pre-trade guard")
    print(f"(solvent under a {STRESS:.0%} adverse move). Realised shocks: "
          f"{SHOCK_MAG:.0%} at rounds {SHOCK_ROUNDS}.")
    print("The ONLY difference is how fast a position may move.\n")

    hdr = f"{'world':<10}{'breaches':>10}{'min net worth':>16}{'peak lev':>11}{'refusals':>10}{'terminal':>12}"
    print(hdr); print("-" * len(hdr))
    for tr in (tp, bd):
        name = "teleport" if tr.mode == "teleport" else "ε-bounded"
        pl = "inf" if tr.peak_leverage == float('inf') else f"{tr.peak_leverage:.2f}"
        print(f"{name:<10}{tr.breach_count:>10}{tr.min_net_worth:>16.2f}"
              f"{pl:>11}{sum(tr.refusals.values()):>10}"
              f"{tr.total_terminal_wealth:>12.1f}")

    print()
    print("FINDINGS")
    if tp.breach_count > 0 and bd.breach_count == 0:
        first = min(b[0] for b in tp.breaches)
        print(f"- The teleporting world passes the same guard and is still")
        print(f"  rendered insolvent (first breach round {first}, min net")
        print(f"  worth {tp.min_net_worth:.2f}). The guard is necessary but")
        print(f"  not sufficient when state can move without bound.")
        print(f"- The ε-bounded world never crosses the floor. Peak leverage")
        print(f"  {bd.peak_leverage:.2f} vs {'inf' if tp.peak_leverage==float('inf') else f'{tp.peak_leverage:.2f}'}:")
        print(f"  bounded motion low-pass filters exposure, so the guard is")
        print(f"  re-evaluated at new prices as the position builds and the")
        print(f"  dangerous state is never reached.")
        print(f"- Mechanism: agents are near-flat BEFORE a crash (valuation")
        print(f"  tracks price) and lever up buying the dip after it. The")
        print(f"  second leg of the decline is what tests solvency.")
    else:
        print("- NEGATIVE RESULT: the teleporting world did not breach under")
        print("  these conditions. Report as such; do not tune to force it.")

    cost = (tp.total_terminal_wealth - bd.total_terminal_wealth) \
        / tp.total_terminal_wealth
    print()
    print("GOVERNANCE COST (headline, reported not hidden)")
    print(f"- ε-bounded terminal wealth is {cost:+.1%} vs teleport "
          f"({bd.total_terminal_wealth:.0f} vs {tp.total_terminal_wealth:.0f}).")
    print(f"- Governance is NOT free: bounded execution forgoes upside in")
    print(f"  calm periods. The teleport total also flatters itself — it")
    print(f"  includes agents that spent {tp.breach_count} agent-rounds")
    print(f"  insolvent, which a real market would have liquidated.")
    print()
    print(f"DSL calls in the governed run: {bd.dsl_calls}")
    print("=" * 72)
    return tp, bd


if __name__ == "__main__":
    main()
