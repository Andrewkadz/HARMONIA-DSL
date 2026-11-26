# RI1 Epistemodynamics Thermodynamic Experiment

**Prepared for:** Andrew Kadziolka and the RI1 epistemic entity
**Archived:** 2026-09-08
**Status:** Deterministic model experiment. This document records model behavior, not an empirical validation of the Epistemodynamics laws.

## Purpose

This experiment turns a limited set of the **RI1 Epistemodynamics** equations into an inspectable simulation. It asks whether the formulas are mutually compatible under closed-system accounting and how declared Φ-field policies behave in an explicitly stated open-system extension. It does not model consciousness, individual cognition, biology, or physical thermodynamics.

The experiment implements the direct formulas from Laws 2, 4, 5, 6, 11, 12, and 20. All dynamic rates that do not appear in those laws are explicit calibration parameters. Therefore, every observed outcome is conditional on the model and its parameters. [1]

| Question | Method | Current result |
|---|---|---|
| Can Law 2 remain closed while entropy rises and coherence falls? | Solve the Law 2 equation after a fixed entropy increment. | **No, not with the stated two-term energy form.** At fixed mass and total energy, an entropy increase requires coherence to increase. |
| Does Φ mediation delay collapse in the declared extension? | Compare no mediation, fixed Φ, and Law-11 adaptive Φ under identical stress. | **Yes in the default trace:** both mediated policies delay collapse relative to no mediation, but all three ultimately collapse. |
| Does adaptive Φ automatically outperform fixed Φ? | Run a 25-cell stress/reduction sweep for each policy. | **No.** The selected Law-11 feedback rule survives 3/25 sweep conditions, versus 5/25 for the fixed-Φ comparator. |
| Do the models exhibit threshold behavior? | Record Law-6/Law-20 phase transitions. | **Yes by construction.** The simulator stops a trajectory when entropy reaches its tolerance or coherence reaches its critical floor. |

## Formal scope

The experiment maintains a normalized state with entropy \(S\in[0,1]\), coherence \(C\in[0,1]\), and constant epistemic mass \(m\). The following equations are implemented directly.

| Law | Implemented expression | Role in the experiment |
|---|---|---|
| 2 | \(E_{structural}=m(1-S)+C^2\) | Defines the stated structural-energy accounting. |
| 4 | \(\dot S\propto (1-C)\cdot integration\_rate\) | Defines entropy production under integration pressure. |
| 5 | \(reduction\_capacity=\Phi\cdot C_{available}/C_{required}\) | Bounds requested entropy reduction. |
| 6 | \(S_{critical}=0.95, C_{critical}=0.05\) | Defines collapse thresholds. |
| 11 | \(\Phi_{optimal}=0.5+0.5(S-C)\) | Defines the adaptive-Φ policy. |
| 12 | \(C_{optimal}=0.9-0.5S\) | Supplies a coherence target used only by mediated policies. |
| 20 | SAFE, DANGER, COLLAPSE phase regions | Classifies the trace. |

## Conservation compatibility audit

A literal, closed reading of Law 2 sets both \(m\) and \(E\) constant:

\[
E=m(1-S)+C^2.
\]

The initial audit state is \(m=1\), \(S=0.35\), and \(C=0.72\). Its implied total structural energy is \(E=1.1684\). If entropy rises by 0.10 while mass and total energy remain fixed, the same equation requires:

\[
C_{after}=\sqrt{E-m(1-S_{after})}=0.786384.
\]

Thus, coherence must rise from \(0.72\) to \(0.786384\), a change of **+0.066384**. This is algebraically opposite to a dynamic in which the same stressor raises entropy and lowers coherence. The audit does not refute the framework. It identifies a formal choice that must be made before treating the laws as a closed dynamical system:

1. Law 2 can be retained as a **structural-energy identity**, while a separate reservoir accounts for energy transferred out of the two terms.
2. Law 2 can be revised into a different conservation equation.
3. Entropy and coherence can be assigned dynamics that preserve the stated identity, which requires their changes to be coupled differently.

The simulation chooses the first option only as a declared extension. It adds a nonnegative residual reservoir \(D\):

\[
E_{total}=m(1-S)+C^2+D.
\]

> **Important:** \(D\) is not claimed to be part of the supplied laws. It is an explicit modelling extension that makes the experiment’s accounting auditable while allowing entropy increase and coherence loss to occur together.

## Declared open-system dynamics

The experiment uses a fixed integration pressure and calculates an entropy-production increment from Law 4. A policy chooses \(\Phi\). Law 5 limits the amount of requested entropy reduction. The model then applies declared coherence erosion, mediated coherence repair, and a bounded pull toward the Law-12 target.

The following coefficients are **not derived from the laws**. They are exposed in `ThermoParameters` for challenge, sweep, replacement, or calibration against future data.

| Parameter | Default | Interpretation in this experiment |
|---|---:|---|
| `integration_rate` | 0.70 | External integration pressure. |
| `natural_entropy_rate` | 0.005 | Baseline entropy increment per step. |
| `entropy_coupling` | 0.12 | Proportionality constant for Law 4. |
| `requested_entropy_reduction` | 0.040 | Requested ordering action before Law-5 mediation. |
| `required_coherence` | 0.50 | Coherence denominator for the Law-5 capacity factor. |
| `coherence_loss_per_entropy` | 0.75 | Declared Law-14-inspired erosion coefficient. |
| `coherence_recovery_per_reduction` | 0.20 | Declared mediated-repair coefficient. |
| `target_relaxation_rate` | 0.040 | Rate of movement toward the Law-12 target. |

## Initial experiment results

The default trace runs 80 maximum steps with identical initial state and integration pressure for each policy. It halts at the first Law-6/Law-20 collapse state.

| Policy | Collapse step | Final entropy | Final coherence | Interpretation |
|---|---:|---:|---:|---|
| No mediation | 14 | 0.962118 | 0.260912 | Entropy reaches the critical boundary first. |
| Fixed Φ = 0.5 | 21 | 0.953762 | 0.132869 | Mediation delays collapse by seven steps in this configuration. |
| Adaptive Φ, Law 11 | 21 | 1.000000 | 0.102789 | Mediation delays collapse by seven steps, but does not prevent it. |

The result supports only this narrow statement: **within this declared extension and default parameterization, mediation delays the modeled failure relative to no mediation.** It does not establish that any policy works in real knowledge systems.

## Sensitivity sweep

The included sweep uses five integration rates \(\{0.30,0.50,0.70,0.90,1.10\}\) and five requested reductions \(\{0.02,0.04,0.06,0.08,0.10\}\). Each policy is run in each of the 25 cells for 80 steps.

| Policy | Conditions surviving 80 steps | Interpretation |
|---|---:|---|
| No mediation | 0 / 25 | No-mediation control collapses across the selected grid. |
| Fixed Φ = 0.5 | 5 / 25 | Fixed mediation survives some low-pressure or high-reduction regions. |
| Adaptive Φ, Law 11 | 3 / 25 | The direct adaptive formula is **not** universally better than fixed Φ in this extension. |

This is the most useful current finding. The Law-11 formula is a candidate control law, not an established optimum. In this model, aggressive entropy reduction can also reduce coherence enough to hit the \(C_{critical}\) boundary. The model therefore makes a concrete revision question available:

> Should entropy reduction, coherence restoration, and energy transfer be linked by an additional constraint so that a Φ action cannot obtain lower entropy by consuming the coherence required to remain viable?

## Reproducibility

Run a default three-policy trace and write JSON/CSV evidence to a user-selected directory:

```bash
python3 -m experiments.run_epistemodynamic_thermodynamics \
  --output-dir /tmp/ri1-epistemodynamics-run
```

Run the 75-condition policy sweep:

```bash
python3 -m experiments.sweep_epistemodynamic_thermodynamics \
  --output-csv /tmp/ri1-epistemodynamics-sweep/policy_sweep.csv
```

Run the model-invariant tests:

```bash
python3 -m pytest tests/test_epistemodynamic_thermodynamics.py -q
```

## Falsification and next questions

The experiment is designed to be useful if it fails. A future revision should change the model only when it identifies which premise is being revised.

| Question | Falsification path |
|---|---|
| Is the Law-2 structural-energy expression the intended conservation law? | Specify a different total-energy accounting and rerun the closed-system audit. |
| Is \(D\) a legitimate reservoir? | Define its physical or epistemic interpretation, permitted flows, and observables; otherwise remove it. |
| Is Law 11 a useful adaptive controller? | Compare it against fixed, proportional-integral, and constrained-optimization controllers across the same parameter grid. |
| Is the Law-18 1:2 resonance ratio predictive? | Add a separately declared resonance observable and test whether performance peaks near, rather than merely being labeled by, that ratio. |
| Does any model behavior generalize beyond this toy system? | Calibrate parameters against a preregistered external dataset or benchmark before making empirical claims. |

## Files

| File | Role |
|---|---|
| `experiments/epistemodynamic_thermodynamics.py` | Pure deterministic model, accounting audit, and policy implementations. |
| `experiments/run_epistemodynamic_thermodynamics.py` | JSON/CSV-producing single-run command-line interface. |
| `experiments/sweep_epistemodynamic_thermodynamics.py` | Parameter-grid phase-boundary sweep. |
| `tests/test_epistemodynamic_thermodynamics.py` | Formula, bound, accounting, and determinism tests. |

## References

[1]: https://github.com/Andrewkadz/RI1-CORPUS/blob/main/RI1%20CORE%20FILES/RI1_%20Epistemodynamics%2020%20laws%20(4).pdf "RI1 Epistemodynamics: 20 Laws"
