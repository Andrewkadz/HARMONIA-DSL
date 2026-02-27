# HARMONIA PROCESSING LAYER — TAU CRYSTAL EDITION
# 17 agents, each with their own Tau Crystal
# Environment: continuous time (NO Tau Crystal)
# Agent 16: KRONOS Singularity Node
# Quantum-accurate: crystallization = wave function collapse (local to each agent)
# Entanglement: emerges from phase-lock between agents, not imposed
# Field seeded by: Andrew Kadziolka EEG (2026-01-29)
# Author: RI1/UOR | Andrew Kadziolka
# License: Unlicense (Public Domain)
# SEED:SELF | 263/97

from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math

# ─────────────────────────────────────────────────────────────────────────────
# FUNDAMENTAL CONSTANTS (ratio-based, no decimal approximations)
# ─────────────────────────────────────────────────────────────────────────────
KSEED       = Fraction(263)
GROOT       = Fraction(97)
FULL_CIRCLE = KSEED + GROOT          # 360
SEED_RATIO  = KSEED / GROOT          # 263/97 — our Euler's number
EPSILON     = Fraction(1, 10)          # dt per step — crystals fire when phase ≥ 1
PHI_APPROX  = Fraction(618, 1000)
PI_APPROX   = Fraction(355, 113)
C_XI        = PHI_APPROX * PI_APPROX # coherence threshold

# EEG field seed (Andrew, 2026-01-29)
EEG = {'delta': 0.398, 'theta': 0.309, 'alpha': 0.186, 'beta': 0.104, 'gamma': 0.003}
GAMMA_F = EEG['gamma']
BETA_F  = EEG['beta']
THETA_F = EEG['theta']

SPEED_FACTOR = 1.0 + GAMMA_F * 20.0   # 1.06
COUPLING_STR = BETA_F * 5.0           # 0.52
FIELD_RADIUS = 5.0 + THETA_F * 10.0   # 8.09


# ─────────────────────────────────────────────────────────────────────────────
# TAU CRYSTAL — private to each agent
# The environment does NOT have one of these.
# ─────────────────────────────────────────────────────────────────────────────
class TauCrystal:
    """
    A discrete time crystal local to one agent.
    Crystallizes (collapses) at its own frequency.
    Stores memory of past crystallizations.
    The environment has no TauCrystal — it runs in continuous time.
    """
    def __init__(self, agent_id, base_frequency_ratio: Fraction):
        self.agent_id = agent_id
        # Each agent gets a unique frequency derived from its id and the seed ratio
        # Agent 16 (KRONOS) gets exactly SEED_RATIO as its base frequency
        if agent_id == 16:
            self.frequency = SEED_RATIO          # 263/97 exactly
        else:
            # Other agents: frequency = SEED_RATIO × (id+1) / 17, as exact ratio
            self.frequency = SEED_RATIO * Fraction(agent_id + 1, 17)

        self.phase = Fraction(0)                 # current phase (exact)
        self.tick_count = 0                      # number of crystallizations
        self.memory = []                         # crystallization events (cyclic truths)
        self._buffer = []                        # pre-crystallization buffer
        self.last_crystallization = None         # state at last crystallization
        self.phase_lock_partners = set()         # agents this crystal is entangled with

    def advance(self, continuous_dt: float) -> bool:
        """
        Advance the crystal by continuous_dt.
        Returns True if a crystallization event occurred.
        """
        # Phase advances by frequency × dt
        dt_frac = Fraction(continuous_dt).limit_denominator(1_000_000)
        self.phase += self.frequency * dt_frac

        # Crystallization occurs when phase crosses an integer boundary
        if self.phase >= 1:
            self.phase -= int(self.phase)   # reset fractional part
            self.tick_count += 1
            return True   # crystallization event
        return False

    def crystallize(self, quantum_state: np.ndarray) -> np.ndarray:
        """
        Collapse the wave function at this crystallization event.
        Returns the collapsed state.
        Stores the event in memory.
        """
        # Measure: collapse to |0> or |1> based on probability
        prob_0 = abs(quantum_state[0])**2
        outcome = 0 if np.random.random() < prob_0 else 1

        if outcome == 0:
            collapsed = np.array([1.0 + 0j, 0.0 + 0j])
        else:
            collapsed = np.array([0.0 + 0j, 1.0 + 0j])

        # Store crystallization event
        event = {
            'tick': self.tick_count,
            'outcome': outcome,
            'prob_0': float(prob_0),
            'phase': float(self.phase),
        }
        self._buffer.append(event)

        # Compress into cyclic truth every GROOT ticks
        if len(self._buffer) >= int(GROOT):
            # Cyclic truth: ratio of |0> outcomes in this cycle
            outcomes = [e['outcome'] for e in self._buffer]
            cyclic_truth = {
                'cycle': len(self.memory),
                'zero_ratio': sum(1 for o in outcomes if o == 0) / len(outcomes),
                'mean_prob_0': sum(e['prob_0'] for e in self._buffer) / len(self._buffer),
                'tick_range': (self._buffer[0]['tick'], self._buffer[-1]['tick']),
            }
            self.memory.append(cyclic_truth)
            self._buffer = []

        self.last_crystallization = collapsed
        return collapsed

    def check_kronos_resonance(self, quantum_state: np.ndarray) -> tuple:
        """
        Check if this crystal's state satisfies the KRONOS condition.
        ΨΩ = |state[0]|² × |state[1]|²
        Φπε = φ × π × ε
        KRONOS resonance: ΨΩ/Φπε expressed as ratio ≈ SEED_RATIO (263/97)
        """
        psi_omega = abs(quantum_state[0])**2 * abs(quantum_state[1])**2

        # After crystallization, ΨΩ = 0 (fully collapsed)
        # We check the PRE-crystallization state for resonance
        phi_pi_eps = float(PHI_APPROX) * float(PI_APPROX) * float(EPSILON)

        if phi_pi_eps > 0 and psi_omega > 0:
            ratio = psi_omega / phi_pi_eps
            # Express distance from seed ratio as fraction of seed ratio
            seed_f = float(SEED_RATIO)
            resonance = abs(ratio - seed_f) / seed_f
        else:
            ratio = 0.0
            resonance = 1.0

        return psi_omega, ratio, resonance


# ─────────────────────────────────────────────────────────────────────────────
# EMERGENT AGENT — with private Tau Crystal
# ─────────────────────────────────────────────────────────────────────────────
class EmergentAgent:
    def __init__(self, agent_id):
        self.id = agent_id
        # Quantum state: superposition |+>
        self.state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        # Private Tau Crystal
        self.tau_crystal = TauCrystal(agent_id, SEED_RATIO)
        # Field position
        self.position = np.random.rand(2) * 10 - 5
        self.velocity = np.random.randn(2) * 0.1
        # KRONOS flag — set by field when resonance achieved
        self.is_kronos = False
        # 6D dimensional state
        self.dimensional_state = np.zeros(6)
        # Entanglement partners (phase-locked tau crystals)
        self.entangled_with = set()

    def evolve_quantum(self, hamiltonian, dt):
        """Unitary evolution between crystallizations"""
        I = np.eye(2, dtype=complex)
        U = I - 1j * hamiltonian * dt
        self.state = np.dot(U, self.state)
        norm = np.linalg.norm(self.state)
        if norm < 1e-9:
            self.state = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        else:
            self.state /= norm

    def step(self, continuous_time: float, hamiltonian, center_mass, coupling_str,
             speed_factor, field_radius) -> dict:
        """
        One continuous-time step.
        The agent's tau crystal may or may not fire.
        """
        dt = float(EPSILON)

        # Check KRONOS resonance BEFORE potential crystallization
        psi_omega, ratio, resonance = self.tau_crystal.check_kronos_resonance(self.state)

        # Evolve quantum state (continuous, unitary)
        self.evolve_quantum(hamiltonian, dt)

        # Advance tau crystal — may trigger crystallization
        crystallized = self.tau_crystal.advance(dt)
        if crystallized:
            # Wave function collapses at this agent's tau tick
            self.state = self.tau_crystal.crystallize(self.state)
            # After collapse, re-enter superposition gradually (decoherence recovery)
            # Mix collapsed state with |+> at rate proportional to field coherence
            recovery = 0.1
            superpos = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
            self.state = (1 - recovery) * self.state + recovery * superpos
            norm = np.linalg.norm(self.state)
            self.state /= norm

        # Evolve field position
        to_center = center_mass - self.position
        alignment = to_center * coupling_str * 0.05
        random_f = np.random.randn(2) * speed_factor * 0.1
        repulsion = self.position * 0.01
        self.velocity += alignment + random_f - repulsion
        self.velocity *= 0.95
        self.position += self.velocity
        dist = np.linalg.norm(self.position)
        if dist > field_radius:
            self.position *= 0.9

        # Update 6D dimensional state using tau crystal's tick count
        tau_t = self.tau_crystal.tick_count
        eps = float(EPSILON)
        fc = float(FULL_CIRCLE)
        for d in range(6):
            h = d + 1
            self.dimensional_state[d] += eps * math.sin(2 * math.pi * tau_t / (fc / h))

        return {
            'crystallized': crystallized,
            'psi_omega': psi_omega,
            'ratio': ratio,
            'resonance': resonance,
            'tau_ticks': self.tau_crystal.tick_count,
        }


# ─────────────────────────────────────────────────────────────────────────────
# PROCESSING LAYER — 17 agents, continuous environment
# ─────────────────────────────────────────────────────────────────────────────
class ProcessingLayer:
    def __init__(self, n_agents=17):
        self.n_agents = n_agents
        np.random.seed(int(KSEED))   # deterministic: seeded by 263
        self.agents = [EmergentAgent(i) for i in range(n_agents)]

        # Environment: continuous time, NO Tau Crystal
        self.continuous_time = 0.0
        self.global_coherence = 0.5
        self.entanglement_entropy = 0.5
        self.karmic_seed = 0.0

        # KRONOS tracking
        self.kronos_emerged = False
        self.kronos_step = None
        self.kronos_resonance_value = None

        # Entanglement tracking (phase-lock detection)
        self.entanglement_pairs = []

        # History
        self.history = {
            'coherence': [], 'entropy': [], 'karmic_seed': [],
            'kronos_resonance': [], 'crystallization_events': [],
            'entanglement_count': [], 'dimensional_means': [],
            'tau_ticks_agent16': [],
        }

    def _hamiltonian(self):
        g = GAMMA_F
        return np.array([[0, g], [g, 0]], dtype=complex)

    def _detect_phase_lock(self):
        """
        Two agents are phase-locked (entangled) when their tau crystal phases
        are within 1/GROOT of each other.
        """
        tolerance = 1.0 / float(GROOT)
        pairs = []
        for i in range(self.n_agents):
            for j in range(i+1, self.n_agents):
                pi = float(self.agents[i].tau_crystal.phase)
                pj = float(self.agents[j].tau_crystal.phase)
                if abs(pi - pj) < tolerance:
                    pairs.append((i, j))
                    self.agents[i].entangled_with.add(j)
                    self.agents[j].entangled_with.add(i)
        self.entanglement_pairs = pairs
        return pairs

    def step(self, step_idx):
        H = self._hamiltonian()
        center_mass = np.mean([a.position for a in self.agents], axis=0)

        crystallization_count = 0
        for agent in self.agents:
            result = agent.step(
                self.continuous_time, H, center_mass,
                COUPLING_STR, SPEED_FACTOR, FIELD_RADIUS
            )
            if result['crystallized']:
                crystallization_count += 1

            # Check KRONOS emergence on agent 16
            if agent.id == 16 and not self.kronos_emerged:
                # KRONOS emerges when resonance < 1/GROOT (within one Groot unit of seed ratio)
                tolerance = 1.0 / float(GROOT)
                if result['resonance'] < tolerance and result['psi_omega'] > 0:
                    self.kronos_emerged = True
                    self.kronos_step = step_idx
                    self.kronos_resonance_value = result['ratio']
                    agent.is_kronos = True
                    print(f"  *** KRONOS EMERGED at step {step_idx} | "
                          f"tau_ticks={result['tau_ticks']} | "
                          f"ratio={result['ratio']:.6f} | "
                          f"resonance={result['resonance']:.6f} ***")

        # Continuous environment metrics (no crystal)
        positions = np.array([a.position for a in self.agents])
        velocities = np.array([a.velocity for a in self.agents])
        std_pos = np.std(positions)
        self.global_coherence = 1.0 / (std_pos + 0.1)
        self.entanglement_entropy = np.mean(np.linalg.norm(velocities, axis=1)) * std_pos

        # Karmic seed (retrocausal accumulation)
        self.karmic_seed += float(EPSILON) * self.global_coherence * float(SEED_RATIO)

        # Detect phase-lock entanglement
        pairs = self._detect_phase_lock()

        # Advance continuous time
        self.continuous_time += float(EPSILON)

        # Record history
        dim_means = np.mean([a.dimensional_state for a in self.agents], axis=0)
        agent16 = self.agents[16]
        _, ratio16, resonance16 = agent16.tau_crystal.check_kronos_resonance(agent16.state)

        self.history['coherence'].append(self.global_coherence)
        self.history['entropy'].append(self.entanglement_entropy)
        self.history['karmic_seed'].append(self.karmic_seed)
        self.history['kronos_resonance'].append(resonance16)
        self.history['crystallization_events'].append(crystallization_count)
        self.history['entanglement_count'].append(len(pairs))
        self.history['dimensional_means'].append(dim_means.copy())
        self.history['tau_ticks_agent16'].append(agent16.tau_crystal.tick_count)

    def run(self, n_steps=3600):
        print("HARMONIA Processing Layer — Tau Crystal Edition")
        print(f"17 agents | each with private TauCrystal | environment: continuous")
        print(f"Agent 16 TauCrystal frequency: {KSEED}/{GROOT} = {float(SEED_RATIO):.6f}")
        print(f"EEG seed: gamma={EEG['gamma']:.3f} beta={EEG['beta']:.3f} theta={EEG['theta']:.3f}")
        print(f"Running {n_steps} steps...")
        print()

        for i in range(n_steps):
            self.step(i)
            if i % 720 == 0:
                a16 = self.agents[16]
                print(f"  Step {i:5d} | coh={self.history['coherence'][-1]:.4f} | "
                      f"ent_pairs={self.history['entanglement_count'][-1]} | "
                      f"crystals={self.history['crystallization_events'][-1]} | "
                      f"a16_ticks={a16.tau_crystal.tick_count} | "
                      f"KRONOS_res={self.history['kronos_resonance'][-1]:.4f}")

        print()
        if self.kronos_emerged:
            print(f"RESULT: KRONOS EMERGED at step {self.kronos_step}")
            print(f"  Ratio at emergence: {self.kronos_resonance_value:.6f}")
            print(f"  Target (263/97): {float(SEED_RATIO):.6f}")
        else:
            min_res = min(self.history['kronos_resonance'])
            print(f"RESULT: KRONOS DID NOT EMERGE")
            print(f"  Closest resonance: {min_res:.6f} (threshold: {1/float(GROOT):.6f})")

        total_crystals = sum(len(a.tau_crystal.memory) for a in self.agents)
        total_cyclic_truths = sum(len(a.tau_crystal.memory) for a in self.agents)
        print(f"Total cyclic truths compressed: {total_crystals}")
        print(f"Karmic seed: {self.karmic_seed:.8f}")
        print(f"Entanglement pairs detected: {len(self.entanglement_pairs)}")
        print(f"Agent 16 tau ticks: {self.agents[16].tau_crystal.tick_count}")
        print(f"Agent 16 cyclic truths: {len(self.agents[16].tau_crystal.memory)}")


# ─────────────────────────────────────────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────────────────────────────────────────
def visualize(layer: ProcessingLayer, output_path: str):
    steps = len(layer.history['coherence'])
    t = np.arange(steps)
    dim_means = np.array(layer.history['dimensional_means'])

    fig = plt.figure(figsize=(22, 15), facecolor='#050510')
    fig.suptitle(
        'HARMONIA Processing Layer — Tau Crystal Edition\n'
        f'17 Agents × Private TauCrystal | Environment: Continuous | '
        f'Agent 16 = KRONOS (freq: {KSEED}/{GROOT})',
        color='#c8a96e', fontsize=13, fontweight='bold', y=0.99
    )

    gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.5, wspace=0.38)

    accent     = '#00ff88'
    kronos_col = '#ff6b35'
    dim_cols   = ['#4fc3f7','#81c784','#ce93d8','#ffb74d','#f06292','#80cbc4']
    dim_labels = ['Math(97)','Physics(85)','Futures(75)','Comms','Impl(20)','Meta']

    def style(ax, title):
        ax.set_facecolor('#0d0d1a')
        ax.set_title(title, color='#aaaacc', fontsize=9)
        ax.tick_params(colors='#555577', labelsize=7)
        for sp in ax.spines.values():
            sp.set_color('#222244')

    def vline(ax):
        if layer.kronos_emerged:
            ax.axvline(layer.kronos_step, color=kronos_col, lw=1.5, ls='--', alpha=0.7)

    # 1. Coherence & Entropy
    ax = fig.add_subplot(gs[0, 0])
    style(ax, 'Field Coherence & Entropy')
    ax.plot(t, layer.history['coherence'], color=accent, lw=1.2, label='Coherence')
    ax.plot(t, layer.history['entropy'], color='#ff5555', lw=1.2, label='Entropy', alpha=0.8)
    vline(ax)
    ax.legend(fontsize=7, facecolor='#1a1a2e', labelcolor='white')

    # 2. KRONOS Resonance
    ax2 = fig.add_subplot(gs[0, 1])
    style(ax2, 'KRONOS Resonance (Agent 16 TauCrystal)')
    ax2.plot(t, layer.history['kronos_resonance'], color=kronos_col, lw=1.2)
    threshold = 1.0 / float(GROOT)
    ax2.axhline(threshold, color='#ffdd00', lw=1.5, ls='--',
                label=f'Threshold 1/{GROOT}={threshold:.4f}')
    ax2.axhspan(0, threshold, alpha=0.1, color='#ffdd00')
    vline(ax2)
    if layer.kronos_emerged:
        ax2.scatter([layer.kronos_step], [layer.history['kronos_resonance'][layer.kronos_step]],
                    color=kronos_col, s=120, zorder=5, marker='*')
    ax2.legend(fontsize=7, facecolor='#1a1a2e', labelcolor='white')

    # 3. Crystallization Events per step
    ax3 = fig.add_subplot(gs[0, 2])
    style(ax3, 'Crystallization Events / Step')
    ax3.plot(t, layer.history['crystallization_events'], color='#c792ea', lw=1.0, alpha=0.8)
    ax3.axhline(np.mean(layer.history['crystallization_events']),
                color='#ffdd00', lw=1, ls='--', label='Mean')
    vline(ax3)
    ax3.legend(fontsize=7, facecolor='#1a1a2e', labelcolor='white')

    # 4. Entanglement (phase-lock pairs)
    ax4 = fig.add_subplot(gs[0, 3])
    style(ax4, 'Emergent Entanglement (Phase-Lock Pairs)')
    ax4.plot(t, layer.history['entanglement_count'], color='#69db7c', lw=1.0)
    vline(ax4)

    # 5. 6D Dimensional Evolution
    ax5 = fig.add_subplot(gs[1, :3])
    style(ax5, '6D HARMONIA Dimensional Evolution (Processing Layer Mean)')
    for d in range(6):
        ax5.plot(t, dim_means[:, d], color=dim_cols[d], lw=1.1,
                 label=dim_labels[d], alpha=0.85)
    vline(ax5)
    ax5.legend(fontsize=7, facecolor='#1a1a2e', labelcolor='white', ncol=6)

    # 6. Agent 16 Tau Ticks
    ax6 = fig.add_subplot(gs[1, 3])
    style(ax6, 'Agent 16 (KRONOS) Tau Crystal Ticks')
    ax6.plot(t, layer.history['tau_ticks_agent16'], color=kronos_col, lw=1.2)
    vline(ax6)

    # 7. Agent positions
    ax7 = fig.add_subplot(gs[2, 0])
    style(ax7, 'Final Agent Positions')
    positions = np.array([a.position for a in layer.agents])
    colors_a = [kronos_col if a.is_kronos else accent for a in layer.agents]
    sizes_a  = [200 if a.is_kronos else 40 for a in layer.agents]
    ax7.scatter(positions[:, 0], positions[:, 1], c=colors_a, s=sizes_a, alpha=0.85, zorder=3)
    circle = plt.Circle((0, 0), FIELD_RADIUS, fill=False, color='#333355', lw=1)
    ax7.add_patch(circle)
    ax7.set_aspect('equal')
    for a in layer.agents:
        if a.is_kronos:
            ax7.annotate('KRONOS', a.position, xytext=(5, 5),
                         textcoords='offset points', color=kronos_col, fontsize=8)

    # 8. Tau Crystal frequency distribution
    ax8 = fig.add_subplot(gs[2, 1])
    style(ax8, 'TauCrystal Frequencies (per agent)')
    freqs = [float(a.tau_crystal.frequency) for a in layer.agents]
    colors_f = [kronos_col if a.id == 16 else '#4fc3f7' for a in layer.agents]
    ax8.bar(range(17), freqs, color=colors_f, alpha=0.85)
    ax8.axhline(float(SEED_RATIO), color='#ffdd00', lw=1.5, ls='--',
                label=f'263/97={float(SEED_RATIO):.3f}')
    ax8.set_xticks(range(17))
    ax8.set_xticklabels([str(i) for i in range(17)], fontsize=6)
    ax8.legend(fontsize=7, facecolor='#1a1a2e', labelcolor='white')

    # 9. Karmic seed
    ax9 = fig.add_subplot(gs[2, 2])
    style(ax9, 'Karmic Seed (Retrocausal Memory)')
    ax9.plot(t, layer.history['karmic_seed'], color='#c792ea', lw=1.2)
    vline(ax9)

    # 10. EEG seed
    ax10 = fig.add_subplot(gs[2, 3])
    style(ax10, 'EEG Field Seed (Andrew 2026-01-29)')
    bands = list(EEG.keys())
    vals  = list(EEG.values())
    bcols = ['#4a90d9','#7b68ee','#98d8c8','#f0a500','#ff6b6b']
    bars  = ax10.bar(bands, vals, color=bcols, alpha=0.85)
    for bar, v in zip(bars, vals):
        ax10.text(bar.get_x() + bar.get_width()/2, v + 0.005,
                  f'{v:.1%}', ha='center', va='bottom', color='white', fontsize=7)

    # Footer
    status = (f"KRONOS EMERGED @ step {layer.kronos_step}"
              if layer.kronos_emerged else "KRONOS: NOT YET EMERGED")
    ent_count = len(layer.entanglement_pairs)
    total_ct  = sum(len(a.tau_crystal.memory) for a in layer.agents)
    fig.text(0.5, 0.005,
             f'{status} | Entangled pairs: {ent_count} | '
             f'Cyclic truths: {total_ct} | Karmic seed: {layer.karmic_seed:.6f} | '
             f'Seed: {KSEED}/{GROOT} | SEED:SELF',
             ha='center', color='#555577', fontsize=8)

    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#050510')
    plt.close()
    print(f"Visualization saved: {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    layer = ProcessingLayer(n_agents=17)
    layer.run(n_steps=3600)   # 10× full circle for tau crystal to accumulate

    output = '/home/ubuntu/HARMONIA_tau_swarm.png'
    visualize(layer, output)

    print()
    print("=" * 65)
    print("PROCESSING LAYER — TAU CRYSTAL SUMMARY")
    print("=" * 65)
    print(f"Agent 16 (KRONOS) TauCrystal frequency: {KSEED}/{GROOT}")
    print(f"Agent 16 tau ticks: {layer.agents[16].tau_crystal.tick_count}")
    print(f"Agent 16 cyclic truths: {len(layer.agents[16].tau_crystal.memory)}")
    print(f"KRONOS emerged: {layer.kronos_emerged}")
    if layer.kronos_emerged:
        print(f"  Emergence step: {layer.kronos_step}")
        print(f"  Resonance ratio: {layer.kronos_resonance_value:.6f}")
        print(f"  Target (263/97): {float(SEED_RATIO):.6f}")
    print(f"Total entanglement pairs (final): {len(layer.entanglement_pairs)}")
    print(f"Total cyclic truths (all agents): {sum(len(a.tau_crystal.memory) for a in layer.agents)}")
    print(f"Karmic seed: {layer.karmic_seed:.8f}")
    print(f"Continuous time elapsed: {layer.continuous_time:.6f}")
    print("=" * 65)
