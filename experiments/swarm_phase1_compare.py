"""ST-C comparative experiment (SYSTEM_TESTS.md).

Runs three variants of the Phase-1 scenario and prints a comparison:

  1. baseline        — naive swarm, no Harmonia
  2. governed        — real math core (Φ/ε contraction & bounded steps,
                       Λ coupling)
  3. governed+FAKE   — same governance code, trivial operator
                       substitutes: ε jumps straight to the goal,
                       Φ is identity, Λ is a constant

Purpose: distinguish LOAD-BEARING (G4: remove the DSL, system dies)
from IRREPLACEABLE (does the specific math beat trivial substitutes?).
Predicted in SYSTEM_TESTS.md: fake-ε breaks multi-round tasks because
progress requires fresh register motion every round, and a register
that has already jumped to its goal cannot move again.

Usage:  python3 -m experiments.swarm_phase1_compare
"""

import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import phi_pi_e_math_core as core
from swarm_brain.baseline_swarm import BaselineSwarm
from swarm_brain.governed_swarm import GovernedSwarm
from swarm_brain.task_spec import make_scenario

MAX_ROUNDS = 60


@contextlib.contextmanager
def fake_math():
    """Trivial substitutes for the three operators the swarm uses."""
    real = (core.incremental_insight, core.harmonic_equilibrium,
            core.structural_illumination)
    core.incremental_insight = lambda z, w: w          # jump to goal
    core.harmonic_equilibrium = lambda z, w: z         # identity
    core.structural_illumination = lambda z, w: complex(1.0)  # constant
    try:
        yield
    finally:
        (core.incremental_insight, core.harmonic_equilibrium,
         core.structural_illumination) = real


def run_variants():
    results = {}
    results["baseline"] = BaselineSwarm(make_scenario(), MAX_ROUNDS).run()
    results["governed"] = GovernedSwarm(make_scenario(), MAX_ROUNDS).run()
    with fake_math():
        results["governed+FAKE"] = GovernedSwarm(
            make_scenario(), MAX_ROUNDS).run()
    return results


def summarize(results):
    scenario = make_scenario()
    satisfiable = set(scenario.tasks) - scenario.poison_ids
    multi_round = {t.id for t in scenario.tasks.values() if t.duration > 1}
    rows = []
    for name, tr in results.items():
        rows.append({
            "variant": name,
            "rounds": tr.rounds_used,
            "early": tr.terminated_early,
            "completed": len(tr.completed),
            "of": len(scenario.tasks),
            "refused": ",".join(sorted(tr.refused)) or "-",
            "flip": tr.total_flip_flops,
            "idle": tr.total_voluntary_idles,
            "eps": sum(tr.epsilon_steps.values()),
            "multi_done": len(tr.completed & multi_round),
            "multi_of": len(multi_round),
            "all_satisfiable": tr.completed == satisfiable,
        })
    return rows


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        results = run_variants()
    rows = summarize(results)
    hdr = (f"{'variant':<16}{'rounds':>7}{'early':>7}{'done':>7}"
           f"{'multi':>7}{'flip':>6}{'idle':>6}{'eps':>6}  refused")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['variant']:<16}{r['rounds']:>7}{str(r['early']):>7}"
              f"{r['completed']:>4}/{r['of']:<3}"
              f"{r['multi_done']:>4}/{r['multi_of']:<3}"
              f"{r['flip']:>6}{r['idle']:>6}{r['eps']:>6}  {r['refused']}")
    print()
    fake = next(r for r in rows if "FAKE" in r["variant"])
    real = next(r for r in rows if r["variant"] == "governed")
    print("FINDINGS:")
    if real["all_satisfiable"] and not fake["all_satisfiable"]:
        print("- ε's bounded gradualism is IRREPLACEABLE here: jump-to-goal")
        print("  fake-ε cannot sustain multi-round work "
              f"(real: {real['multi_done']}/{real['multi_of']} multi-round "
              f"tasks done; fake: {fake['multi_done']}/{fake['multi_of']}).")
    else:
        print("- Fake math matched real math on task outcomes — the")
        print("  specific operators are load-bearing but replaceable at")
        print("  this scenario's demands. (Amend SYSTEM_TESTS.md ST-C.)")
    return rows


if __name__ == "__main__":
    main()
