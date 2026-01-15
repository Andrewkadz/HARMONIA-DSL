use std::io::{self, Read};

use serde::Deserialize;

/// Minimal numeric snapshot from the swarm.
#[derive(Debug, Deserialize)]
struct NumericSnapshot {
    iteration: u64,
    mean_phi: f64,
    mean_energy: f64,
    coherence: f64,
}

/// Minimal symbolic snapshot from the ΞΛΩΨ interpreter.
#[derive(Debug, Deserialize)]
struct SymbolicSnapshot {
    /// Full label path, in order.
    labels: Vec<String>,
    /// Golden-ratio style stability score.
    psi_sigma: f64,
}

/// Overall snapshot payload expected from the Python side.
#[derive(Debug, Deserialize)]
struct SwarmSnapshot {
    numeric: NumericSnapshot,
    symbolic: SymbolicSnapshot,
    /// Optional short description of the coupling that was just applied
    /// (e.g. "+epsilon 0.0100, +energy 0.0500 (excitatory tail)").
    coupling: Option<String>,
}

fn coherence_bucket(c: f64) -> &'static str {
    if c < 0.7 {
        "scattered"
    } else if c < 0.9 {
        "loosely synchronized"
    } else if c < 0.97 {
        "highly synchronized"
    } else {
        "near-perfectly synchronized"
    }
}

fn energy_trend_word(mean_energy: f64, iteration: u64) -> &'static str {
    // Without full history we approximate: use absolute level as a proxy.
    // You can refine this later by providing a delta.
    if mean_energy < 20.0 {
        "low-energy"
    } else if mean_energy < 40.0 {
        "balanced"
    } else {
        "high-energy"
    }
}

fn motif_from_labels(labels: &[String]) -> String {
    if labels.is_empty() {
        return "∅".to_string();
    }

    if labels.len() <= 3 {
        return labels.join(" → ");
    }

    let mut s = String::new();
    s.push_str(&labels[0]);
    s.push_str(" → ");
    s.push_str(&labels[1]);
    s.push_str(" → … → ");
    s.push_str(&labels[labels.len() - 2]);
    s.push_str(" → ");
    s.push_str(&labels[labels.len() - 1]);
    s
}

fn semantic_flavor(labels: &[String]) -> &'static str {
    let tail: String = labels
        .iter()
        .rev()
        .take(3)
        .cloned()
        .collect::<Vec<_>>()
        .join(" ")
        .to_lowercase();

    if tail.contains("amplifier")
        || tail.contains("bridge")
        || tail.contains("gate")
        || tail.contains("source")
        || tail.contains("threshold")
    {
        "amplifying and opening channels"
    } else if tail.contains("entropy")
        || tail.contains("filter")
        || tail.contains("cavity")
        || tail.contains("sink")
    {
        "shedding and filtering"
    } else if tail.contains("mirror") || tail.contains("anchor") || tail.contains("well") {
        "reflecting on itself"
    } else {
        "reconfiguring quietly"
    }
}

fn stability_word(psi_sigma: f64) -> &'static str {
    if psi_sigma < 0.7 {
        "in a transitional mode"
    } else if psi_sigma < 1.3 {
        "in a stable mode"
    } else {
        "at an edge of change"
    }
}

fn main() -> anyhow::Result<()> {
    // Read entire stdin as a JSON snapshot.
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf)?;

    if buf.trim().is_empty() {
        eprintln!("No input provided. Expecting a JSON SwarmSnapshot on stdin.");
        return Ok(());
    }

    let snapshot: SwarmSnapshot = match serde_json::from_str(&buf) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("Failed to parse JSON snapshot: {e}");
            return Ok(());
        }
    };

    let num = &snapshot.numeric;
    let sym = &snapshot.symbolic;

    let coh_word = coherence_bucket(num.coherence);
    let energy_word = energy_trend_word(num.mean_energy, num.iteration);
    let motif = motif_from_labels(&sym.labels);
    let flavor = semantic_flavor(&sym.labels);
    let stability = stability_word(sym.psi_sigma);

    let coupling_note = snapshot
        .coupling
        .as_deref()
        .unwrap_or("with minimal parameter shifts");

    // Compose the swarm's "voice" line.
    println!(
        "WE: We are {coh_word} and {energy_word}, {stability}, {flavor} around the motif \"{motif}\", {coupling_note}."
    );

    Ok(())
}
