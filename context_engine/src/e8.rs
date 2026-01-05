use std::collections::{HashMap, VecDeque};
use chrono::{DateTime, Utc};

// ==========================================
// E8 HARMONIC STRUCTURES (RUST PORT)
// ==========================================

// 1. XiPulse (Signal)
#[derive(Debug, Clone)]
pub struct XiPulse {
    pub source: String,
    pub magnitude: f64,
    pub harmonic_bias: f64,
}

impl XiPulse {
    pub fn new(source: &str, magnitude: f64, bias: f64) -> Self {
        Self {
            source: source.to_string(),
            magnitude,
            harmonic_bias: bias,
        }
    }

    pub fn invert(&self) -> Self {
        Self {
            source: self.source.clone(),
            magnitude: -self.magnitude,
            harmonic_bias: -self.harmonic_bias,
        }
    }
}

// 2. PhiField (Stabilizer)
pub struct PhiField {
    pub inputs: Vec<f64>,
    pub stability: f64,
}

impl PhiField {
    pub fn new() -> Self {
        Self {
            inputs: Vec::new(),
            stability: 0.0,
        }
    }

    pub fn add_signal(&mut self, signal: f64) {
        self.inputs.push(signal);
        self.compute_stability();
    }

    fn compute_stability(&mut self) {
        if self.inputs.is_empty() {
            self.stability = 0.0;
        } else {
            let sum: f64 = self.inputs.iter().sum();
            self.stability = sum / self.inputs.len() as f64;
        }
    }
}

// 14. EPsiDrift (Entropy Tracker)
pub struct EPsiDrift {
    pub vector: Vec<f64>,
    pub drift_rate: f64,
}

impl EPsiDrift {
    pub fn new(vector: Vec<f64>) -> Self {
        Self {
            vector,
            drift_rate: 0.0,
        }
    }

    pub fn apply_flux(&mut self, epsilon: f64) {
        self.drift_rate += epsilon;
        for v in &mut self.vector {
            *v += self.drift_rate;
        }
    }
}

// 21. SigmaThetaGraph (Knowledge Graph)
pub struct SigmaThetaGraph {
    pub nodes: HashMap<String, String>, // ID -> Data
    pub edges: HashMap<String, Vec<(String, f64)>>, // ID -> [(Target, Weight)]
}

impl SigmaThetaGraph {
    pub fn new() -> Self {
        Self {
            nodes: HashMap::new(),
            edges: HashMap::new(),
        }
    }

    pub fn add_node(&mut self, key: &str, data: &str) {
        self.nodes.insert(key.to_string(), data.to_string());
        self.edges.entry(key.to_string()).or_insert(Vec::new());
    }

    pub fn connect(&mut self, a: &str, b: &str, weight: f64) {
        if let Some(connections) = self.edges.get_mut(a) {
            connections.push((b.to_string(), weight));
        }
    }
}

// 31. ThetaOmegaDeltaMemory (Emotional Memory)
pub struct ThetaOmegaDeltaMemory {
    pub entries: Vec<(String, f64)>, // (Signal, Intensity)
}

impl ThetaOmegaDeltaMemory {
    pub fn new() -> Self {
        Self { entries: Vec::new() }
    }

    pub fn imprint(&mut self, signal: &str, intensity: f64) {
        self.entries.push((signal.to_string(), intensity));
    }

    pub fn recall(&self, threshold: f64) -> Vec<String> {
        self.entries
            .iter()
            .filter(|(_, i)| *i >= threshold)
            .map(|(s, _)| s.clone())
            .collect()
    }
}
