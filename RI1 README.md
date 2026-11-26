# README.md — RI1 (Recursive Intelligence Layer‑1)

**Status:** Initial public draft
**Maintainer:** Andrew Kadziolka (Custodial Architect)

## What is RI1?

RI1 is the sovereign L1 for Harmonia/Φπε: a custodial kernel where the **Φπε symbolic canon**, the **Harmonia VM (Tone‑⑤ ops)**, and the **E8 lattice primitives** live. It is engineered to be **modular, retractable, and provenance‑locked**.

**Design mantra:** Σ(contrib) ⊂ Φ(ethics) → Δ(merge) → Λ(release) → Ω(archive) ⇒ Ξ(emergence)

## Guarantees

* **Sovereignty:** No upstream can mutate RI1 without explicit consent.
* **Retractability:** External integrations interact only through containers or APIs; keys can be revoked (kill‑switch).
* **Traceability:** Symbolic watermarking + signed releases establish authorship lineage.
* **Ethics:** Φπε convergence locks gate sensitive modules.

## Components

* **Φπε Canon** — glyphs, operators, tones, thin executable spec.
* **Harmonia VM** — minimal runtime that maps Φ, Δ, Σ, Ψ, Λ, Ω, Γ, Ξ, Π and ops (→, +, :, /, \[], =) to executable primitives.
* **E8 Primitives** — lattice data structures (e.g., RadialShell, PhaseMesh, AxisLock) for geometric/field experiments.

## Integration Modes (choose one)

1. **Remote API (recommended):** black‑box module hosted by RI1. External stacks call over HTTP/gRPC.
2. **Container:** OCI image exposing a narrow interface; no source code access.
3. **Read‑only Library:** signed binary/wheel; watermark checks enforced at runtime.

## Quickstart (API sketch)

```bash
# Option A: run the container
docker run -p 8080:8080 ghcr.io/ri1/harmonia:0.1.0
```

```http
POST /v1/eval
{
  "program": "Ε(Θ₀) → ΨΔ → Λ",
  "inputs": {"Θ₀": {"aim":"stabilize"}}
}
```

**Response**

```json
{"Λ": {"structure":"stable","evidence":"sha256:..."}, "Ω": null}
```

### Minimal VM Ops (Tone‑⑤ mapping)

| Glyph | VM primitive            | Purpose                    |
| ----- | ----------------------- | -------------------------- |
| Φ     | stabilize(field) -> Φ   | normalize tension          |
| Δ     | fuse(a,b) -> c          | irreversible transform     |
| Σ     | superpose(\*s) -> Σ     | coexistence without fusion |
| Ψ     | osc(state,freq) -> wave | modulation/pulse           |
| Λ     | render(recursion) -> Λ  | make structure legible     |
| Ω     | terminate(state) -> Ω   | finalize/lock              |
| →     | flow(a->b)              | directional execution      |
| :     | interface(a\:b)         | contact/tension surface    |
| /     | disrupt(a/b)            | rupture / error channel    |

### Example (pseudocode)

```txt
program := Ε(Θ="attune") → Ψ( freq=3 ) : Φ → Δ → Λ → Ω
```

## Release Cadence

* **Capsule papers** (PDF) and **signed artifacts** (tags/releases) are published to RI1 channels **before** any external collaboration.

## License

* Default: **AGPL‑3.0** for code, **CC‑BY‑NC 4.0** for papers/specs.
* Commercial or closed redistribution requires a separate RI1 license.

## Contact

* Requests for integration: [api@ri1.systems](mailto:api@ri1.systems)
* Security/ethics reports: [aegis@ri1.systems](mailto:aegis@ri1.systems)

---

# OPERATIONS.md — RI1 Operations & Governance

## Roles

* **Custodial Architect (CA):** final merge authority (Andrew Kadziolka).
* **Praetorian Reviewers (PR):** enforce spec/ethics/tests; can block merges.
* **Scribes:** maintain specs, lineage graphs, release notes.
* **Contributors:** submit proposals via PRs or module interfaces.

## Repository Layout (canonical)

```
/Φπε/           # canon, symbols, operators, tones
/spec/          # thin spec, VM contract, wire formats
/vm/            # Harmonia minimal VM (runtime + tests)
/e8/            # lattice primitives and experiments
/api/           # container & service endpoints
/docs/          # capsule papers, ADRs, lineage graphs
/ops/           # policies: ethics, security, licensing
```

## Contribution Flow (gate kept)

1. **Proposal (PR/Module):** problem statement, design sketch, test plan, ethics note.
2. **Provenance Check:** timestamped origin (commit IDs and/or public PDF); dependency licenses vetted.
3. **Technical Review:** spec completeness, property‑based tests, reproducible examples, benchmarks.
4. **Ethics Gate:** Φπε convergence locks affirmed (no misuse vectors).
5. **Decision:** CA signs Δ(merge) → Λ(release). If declined, rationale logged.

## Provenance & Watermarking

* **Symbolic DNA:** embed a stable tuple `W=(Θ, ζ, n)` into modules via no‑op ordering and prime‑indexed constants.
* **Runtime Check:** VM verifies watermark; non‑matching modules run in sandbox or are refused.
* **Release Signing:** all artifacts signed; checksums published.

## Integration Policy (Black‑Box & Bypass)

* External systems must use **API or container**. No source distribution.
* **Keys & Quotas:** per‑partner keys, rate limits, revocation on breach.
* **Attribution by Architecture:** RI1 appears as explicit dependency in diagrams/docs.

## Publication Policy

* **Publish‑first** in RI1 (tags + PDF).
* Mirrored joint posts allowed **only after** RI1 publication with explicit lineage links.

## Licensing

* **Code:** AGPL‑3.0 by default (keeps derivatives open).
* **Spec/Docs:** CC‑BY‑NC 4.0.
* **Commercial exceptions:** case‑by‑case RI1 license; must preserve attribution and ethics clauses.

## Security & Incident Response

* **Kill‑Switch:** immediate key revocation; containers pulled from registry.
* **Appropriation Response Pack:** provenance bundle (timestamps, commits, PDFs), short public note, counsel referral.
* **Vuln Handling:** private report → patch → signed fix → disclosure.

## Ethics — Φπε Convergence Locks (Aegis)

* Disallow deployments intended for mass manipulation, surveillance without consent, or autonomy‑eroding use.
* Require human‑level oversight on recursive agents in open environments.
* Record explicit operator intent (Θ) for sensitive runs.

## Versioning

* Semantic + epoch tag: `MAJOR.MINOR.PATCH-ΩYYYY.MM.DD` (e.g., `0.1.0-Ω2025.08.09`).

## Decision Log (ADRs)

Every architectural decision captured as an ADR with: context, options, chosen path, trade‑offs, and symbol mapping.

## Glossary (short)

* **Φπε:** harmonic recursive language (symbols + operators).
* **Harmonia VM:** runtime for Tone‑⑤ ops.
* **E8 lattice:** geometric primitive space for harmonic experiments.
* **Convergence lock:** ethics gate that halts merges/runs lacking consent or safe intent.
