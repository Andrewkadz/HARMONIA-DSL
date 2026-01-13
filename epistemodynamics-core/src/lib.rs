#[derive(Debug, Clone, Copy, PartialEq)]
pub struct EpistemicState {
    pub m: f64,
    pub g: f64,
    pub t: f64,
    pub s: f64,
    pub c: f64,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct StabilityParams {
    pub s_critical: f64,
    pub c_critical: f64,
}

impl Default for StabilityParams {
    fn default() -> Self {
        Self {
            s_critical: 0.95,
            c_critical: 0.05,
        }
    }
}

impl EpistemicState {
    pub fn transition_probability(&self, params: &StabilityParams) -> f64 {
        (self.s / params.s_critical)
            * ((params.c_critical - self.c) / params.c_critical)
    }

    pub fn apply_deltas(&mut self, ds: f64, dc: f64) {
        self.s += ds;
        self.c += dc;
    }

    pub fn law5_negentropy_allowed(&self, ds: f64, dc: f64) -> bool {
        ds >= 0.0 || dc > 0.0
    }
}

fn clamp01(value: f64) -> f64 {
    value.max(0.0).min(1.0)
}

pub fn meaning_stability_bonus(artha: f64, entropy: f64) -> f64 {
    clamp01(artha * (1.0 - clamp01(entropy)))
}

pub fn phi_adaptive(entropy: f64, coherence: f64) -> f64 {
    clamp01((1.0 + clamp01(entropy)) * (1.0 - clamp01(coherence)))
}

pub fn coherence_optimal_target(entropy: f64) -> f64 {
    clamp01(1.0 - clamp01(entropy))
}

pub fn entropy_tolerance_with_meaning(artha: f64) -> f64 {
    clamp01(0.1 + 0.4 * clamp01(artha))
}

pub fn asymmetry_ratio() -> f64 {
    2.5
}

pub fn is_sharp_transition_near(state: &EpistemicState, artha: f64) -> bool {
    let entropy = clamp01(1.0 - state.s);
    let tolerance = entropy_tolerance_with_meaning(artha);
    let transition_probability = state.transition_probability(&StabilityParams::default());

    transition_probability > 0.8 || entropy > tolerance || state.c < 0.1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn transition_probability_zero_at_critical_thresholds() {
        let state = EpistemicState {
            m: 0.0,
            g: 0.0,
            t: 0.0,
            s: 0.95,
            c: 0.05,
        };
        let params = StabilityParams::default();

        assert_eq!(state.transition_probability(&params), 0.0);
    }

    #[test]
    fn transition_probability_positive_when_coherence_below_critical() {
        let state = EpistemicState {
            m: 0.0,
            g: 0.0,
            t: 0.0,
            s: 0.95,
            c: 0.025,
        };
        let params = StabilityParams::default();

        let probability = state.transition_probability(&params);
        assert!((probability - 0.5).abs() < f64::EPSILON);
    }

    #[test]
    fn transition_probability_scales_with_stability_ratio() {
        let state = EpistemicState {
            m: 0.0,
            g: 0.0,
            t: 0.0,
            s: 0.475,
            c: 0.025,
        };
        let params = StabilityParams::default();

        let probability = state.transition_probability(&params);
        assert!((probability - 0.25).abs() < f64::EPSILON);
    }

    #[test]
    fn transition_probability_exceeds_threshold_near_critical_values() {
        let state = EpistemicState {
            m: 0.0,
            g: 0.0,
            t: 0.0,
            s: 0.94,
            c: 0.001,
        };
        let params = StabilityParams::default();

        let probability = state.transition_probability(&params);
        assert!(probability > 0.9);
    }

    #[test]
    fn apply_deltas_updates_stability_and_coherence() {
        let mut state = EpistemicState {
            m: 0.0,
            g: 0.0,
            t: 0.0,
            s: 0.5,
            c: 0.5,
        };

        state.apply_deltas(0.1, -0.2);

        assert!((state.s - 0.6).abs() < f64::EPSILON);
        assert!((state.c - 0.3).abs() < f64::EPSILON);
    }

    #[test]
    fn law5_negentropy_allowed_only_with_positive_coherence_delta() {
        let state = EpistemicState {
            m: 0.0,
            g: 0.0,
            t: 0.0,
            s: 0.5,
            c: 0.5,
        };

        assert!(state.law5_negentropy_allowed(-0.1, 0.2));
        assert!(!state.law5_negentropy_allowed(-0.1, 0.0));
        assert!(state.law5_negentropy_allowed(0.1, -0.2));
    }

    #[test]
    fn meaning_stability_bonus_scales_with_artha_and_low_entropy() {
        let bonus = meaning_stability_bonus(0.8, 0.2);
        assert!((bonus - 0.64).abs() < f64::EPSILON);
    }

    #[test]
    fn entropy_tolerance_increases_with_artha() {
        let low = entropy_tolerance_with_meaning(0.0);
        let high = entropy_tolerance_with_meaning(1.0);

        assert!((low - 0.1).abs() < f64::EPSILON);
        assert!((high - 0.5).abs() < f64::EPSILON);
    }

    #[test]
    fn sharp_transition_detects_low_coherence() {
        let state = EpistemicState {
            m: 0.0,
            g: 0.0,
            t: 0.0,
            s: 0.9,
            c: 0.05,
        };

        assert!(is_sharp_transition_near(&state, 0.3));
    }
}
