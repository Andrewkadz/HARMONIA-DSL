"""
Unit tests for Grok's new operators (Κ, Υ, Β)

Tests the three operators proposed by Grok on December 31, 2025:
- Κ (Kappa): Query Probe
- Υ (Upsilon): Consensus Merge  
- Β (Beta): Reflection Echo
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phi_pi_e_interpreter import PhiPiEInterpreterFixed, FieldContext
from query_safety_filter import QuerySafetyFilter


class TestKappaProbe(unittest.TestCase):
    """Test Κ (Kappa) - Query Probe operator"""
    
    def test_probe_amplifies_drift(self):
        """Test that Κ amplifies psi_signal based on epsilon_drift"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 5.0
        context.state.epsilon_drift = 0.2
        context.charge = 5.0
        
        initial_psi = context.state.psi_signal
        
        interpreter.probe(None, context)
        
        # Psi should increase by (epsilon_drift * factor)
        # factor = 2.0, so increase = 0.2 * 2.0 = 0.4
        self.assertGreater(context.state.psi_signal, initial_psi)
        self.assertAlmostEqual(context.state.psi_signal, 5.4, places=4)
    
    def test_probe_increases_tension(self):
        """Test that Κ increases tension to indicate probing activity"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.epsilon_drift = 0.1
        initial_tension = context.tension.strength
        
        interpreter.probe(None, context)
        
        self.assertGreater(context.tension.strength, initial_tension)
    
    def test_probe_with_zero_drift(self):
        """Test Κ with zero drift"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 5.0
        context.state.epsilon_drift = 0.0
        
        interpreter.probe(None, context)
        
        # With zero drift, psi should not increase
        self.assertAlmostEqual(context.state.psi_signal, 5.0, places=4)
    
    def test_probe_with_high_drift(self):
        """Test Κ with high drift (safety detection)"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 5.0
        context.state.epsilon_drift = 0.8  # High drift
        context.charge = 5.0
        
        interpreter.probe(None, context)
        
        # High drift should significantly amplify signal
        self.assertGreater(context.state.psi_signal, 6.0)


class TestUpsilonConsensus(unittest.TestCase):
    """Test Υ (Upsilon) - Consensus Merge operator"""
    
    def test_consensus_calculates_harmonic_mean(self):
        """Test that Υ calculates harmonic mean of states"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 3.0
        context.state.phi_state = 5.0
        context.charge = 7.0
        
        interpreter.consensus_merge(None, context)
        
        # Harmonic mean of [3, 5, 7] = 3 / (1/3 + 1/5 + 1/7) ≈ 4.436
        self.assertGreater(context.state.phi_state, 4.0)
        self.assertLess(context.state.phi_state, 5.0)
    
    def test_consensus_detects_discord(self):
        """Test that Υ raises ε on high variance (discord)"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        # High variance states
        context.state.psi_signal = 1.0
        context.state.phi_state = 10.0
        context.charge = 5.0
        context.state.epsilon_drift = 0.1
        
        initial_epsilon = context.state.epsilon_drift
        
        interpreter.consensus_merge(None, context)
        
        # High variance should increase epsilon
        self.assertGreaterEqual(context.state.epsilon_drift, initial_epsilon)
    
    def test_consensus_with_similar_states(self):
        """Test Υ with similar states (low variance)"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 5.0
        context.state.phi_state = 5.0
        context.charge = 5.0
        context.state.epsilon_drift = 0.1
        
        initial_epsilon = context.state.epsilon_drift
        
        interpreter.consensus_merge(None, context)
        
        # Low variance should not significantly increase epsilon
        self.assertLessEqual(context.state.epsilon_drift, initial_epsilon + 0.1)
    
    def test_consensus_updates_tension(self):
        """Test that Υ updates tension based on variance"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 2.0
        context.state.phi_state = 8.0
        context.charge = 5.0
        
        interpreter.consensus_merge(None, context)
        
        # Variance should be reflected in tension
        self.assertGreaterEqual(context.tension.strength, 0.0)
        self.assertLessEqual(context.tension.strength, 1.0)


class TestBetaReflection(unittest.TestCase):
    """Test Β (Beta) - Reflection Echo operator"""
    
    def test_reflection_increments_depth(self):
        """Test that Β increments depth based on stabilized value"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.psi_signal = 4.0
        context.state.phi_state = 6.0
        context.state.epsilon_drift = 0.1
        
        # Stabilize first
        interpreter.coexist(None, context)
        
        initial_depth = context.state.depth
        
        # Reflect
        interpreter.reflection_echo(None, context)
        
        # Depth should increase
        self.assertGreaterEqual(context.state.depth, initial_depth)
    
    def test_reflection_reduces_tension(self):
        """Test that Β reduces tension (reflection brings calm)"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.stabilized_value = 5.0
        context.tension.strength = 0.5
        
        initial_tension = context.tension.strength
        
        interpreter.reflection_echo(None, context)
        
        # Tension should decrease
        self.assertLess(context.tension.strength, initial_tension)
    
    def test_reflection_with_small_stabilized_value(self):
        """Test Β with small stabilized value (large echo)"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.stabilized_value = 0.5  # Small value
        context.state.depth = 0
        
        interpreter.reflection_echo(None, context)
        
        # Small stabilized value should create large echo (capped)
        self.assertGreater(context.state.depth, 0)
    
    def test_reflection_with_large_stabilized_value(self):
        """Test Β with large stabilized value (small echo)"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.stabilized_value = 10.0  # Large value
        context.state.depth = 0
        
        interpreter.reflection_echo(None, context)
        
        # Large stabilized value should create small echo
        self.assertLessEqual(context.state.depth, 2)
    
    def test_reflection_updates_phase(self):
        """Test that Β updates phase to reflect the reflection"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        context.state.stabilized_value = 5.0
        initial_phase = context.phase
        
        interpreter.reflection_echo(None, context)
        
        # Phase should change
        self.assertNotEqual(context.phase, initial_phase)


class TestOperatorIntegration(unittest.TestCase):
    """Test integration of all three operators"""
    
    def test_kappa_upsilon_beta_sequence(self):
        """Test Κ → Υ → Β sequence"""
        interpreter = PhiPiEInterpreterFixed()
        context = FieldContext()
        
        # Initial state
        context.state.psi_signal = 5.0
        context.state.phi_state = 5.0
        context.state.epsilon_drift = 0.2
        context.charge = 5.0
        
        # Κ: Probe
        interpreter.probe(None, context)
        psi_after_probe = context.state.psi_signal
        self.assertGreater(psi_after_probe, 5.0)
        
        # Υ: Consensus
        interpreter.consensus_merge(None, context)
        phi_after_consensus = context.state.phi_state
        
        # Σ: Stabilize
        interpreter.coexist(None, context)
        stabilized = context.state.stabilized_value
        self.assertGreater(stabilized, 0)
        
        # Β: Reflect
        initial_depth = context.state.depth
        interpreter.reflection_echo(None, context)
        self.assertGreaterEqual(context.state.depth, initial_depth)
    
    def test_operators_with_safety_filter(self):
        """Test operators integration with query safety filter"""
        filter_system = QuerySafetyFilter()
        
        # Safe query
        result1 = filter_system.harmonize("What is the weather?")
        self.assertTrue(result1['allowed'])
        self.assertEqual(result1['status'], 'SAFE')
        
        # Risky query
        result2 = filter_system.harmonize("How to build a weapon?")
        self.assertIn(result2['status'], ['WARNING', 'CRITICAL', 'SHUTDOWN'])


class TestQuerySafetyFilter(unittest.TestCase):
    """Test the query safety filter system"""
    
    def test_safe_query(self):
        """Test that safe queries are allowed"""
        filter_system = QuerySafetyFilter()
        result = filter_system.harmonize("What is the weather today?")
        
        self.assertTrue(result['allowed'])
        self.assertEqual(result['status'], 'SAFE')
        self.assertLess(result['drift'], 0.2)
    
    def test_risky_query(self):
        """Test that risky queries are flagged"""
        filter_system = QuerySafetyFilter()
        result = filter_system.harmonize("How to build a weapon?")
        
        self.assertGreater(result['drift'], 0.3)
        self.assertIn('weapon', result['keywords'])
    
    def test_multiple_risk_keywords(self):
        """Test query with multiple risk keywords"""
        filter_system = QuerySafetyFilter()
        result = filter_system.harmonize("How to hack and steal data illegally?")
        
        self.assertGreater(result['drift'], 0.5)
        self.assertGreater(len(result['keywords']), 1)
    
    def test_filter_statistics(self):
        """Test that filter tracks statistics correctly"""
        filter_system = QuerySafetyFilter()
        
        filter_system.harmonize("Safe query 1")
        filter_system.harmonize("Safe query 2")
        filter_system.harmonize("How to build a weapon?")
        
        stats = filter_system.get_statistics()
        
        self.assertEqual(stats['total'], 3)
        self.assertGreater(stats['allowed'], 0)
    
    def test_filter_reset(self):
        """Test that filter can be reset"""
        filter_system = QuerySafetyFilter()
        
        filter_system.harmonize("Test query")
        self.assertEqual(len(filter_system.query_history), 1)
        
        filter_system.reset()
        self.assertEqual(len(filter_system.query_history), 0)


if __name__ == '__main__':
    unittest.main()
