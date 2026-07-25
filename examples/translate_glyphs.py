# examples/translate_glyphs.py

from φπε_quantum import translate_fpe_sequence, simulate_and_plot

# Example φπε field sequence: superposition, entangle, rotate, stabilize, measure
sequence = "ΨΨΨ ΧΧ ΔΦΣ ΩΩ"

# Translate and simulate
qc = translate_fpe_sequence(sequence, num_qubits=3)
qc.draw('mpl')  # Optional visual before simulate

simulate_and_plot(qc)
