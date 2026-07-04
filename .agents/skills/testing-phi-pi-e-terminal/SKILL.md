---
name: testing-phi-pi-e-terminal
description: Test the Φπε (ΦShell) DSL interpreter end-to-end via the Φπε.py terminal REPL. Use when verifying changes to phi_pi_e_interpreter.py or the ΞΣ symbolic DSL.
---

# Testing the Φπε / ΦShell DSL interpreter

## What this app is
`phi_pi_e_interpreter.py` defines `PhiPiEInterpreter`, the engine for the ΞΣ symbolic DSL.
The user-facing entry point is `Φπε.py` — an interactive terminal REPL that boots a "ΦShell"
banner and routes each typed line through `interpreter.execute(command)`. This is a real
CLI/REPL, so it is best demonstrated visually in a GUI terminal (konsole).

## Setup
- `pip install -r requirements.txt` (needs `numpy`; the blueprint installs it).
- No secrets/credentials required. **Devin Secrets Needed:** none.
- `Φπε.py` requires `NEXUS.hrm` and (optionally) `Φπε_loader.hrm`, both in the repo root.

## Fast sanity checks (shell, no recording)
```
python3 test_phi_pi_e.py              # execute path; expect "Result: ['Φ']"
printf 'Φ\nexit\n' | python3 Φπε.py   # REPL boots and runs headlessly
python3 -c "from phi_pi_e_interpreter import PhiPiEInterpreter as P; print(P().loop([1,2,3]))"  # expect 3, not RecursionError
```

## GUI end-to-end (record this)
Compare pre-change vs post-change to make a broken build visibly different:
1. Create a worktree of the base branch in a **persistent** dir (NOT /tmp — it is wiped on
   VM restart): `git worktree add ~/harm-main origin/main`.
2. Launch konsole, maximize with `wmctrl -r :ACTIVE: -b add,maximized_vert,maximized_horz`.
3. Run `python3 ~/harm-main/Φπε.py` → on a broken build this crashes at line 5
   (`PhiPiEInterpreter()`); on a good build the `ΞΣ_TERM[Φπε] >>` prompt appears.
4. Run `python3 ~/repos/HARMONIA-DSL/Φπε.py`, type `Φ` (expect result `['Φ']`), then `exit`.

## CRITICAL gotcha: typing Greek/ΞΣ symbols
The DSL uses non-ASCII symbols (Φ, Π, Σ, Θ, →). The computer-tool `type` action and
`xdotool type` DROP these characters. Enter them via the clipboard instead:
```
printf 'python3 ~/repos/HARMONIA-DSL/Φπε.py' | DISPLAY=:0 xclip -selection clipboard
```
then paste in konsole with **Ctrl+Shift+V**. `xclip` may need `apt-get install -y xclip`.

## Out of scope / known-bad
- `test_interpreter.py` targets an older, self-contradictory API (calls `stabilize` with 1
  and 2 args, uses `interpreter.FieldContext()`, reads a nonexistent `~/Downloads/*.hrm`).
  It cannot fully pass without editing the test — don't treat its failures as regressions.
- `streamlit_app.py` uses `OllamaAgent` (needs a local Ollama server) and does NOT import
  the interpreter, so it can't validate interpreter changes.
