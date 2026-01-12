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
}
