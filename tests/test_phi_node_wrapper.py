"""
Integration tests for ΦπεNode wrapper classes

Tests backward compatibility with Phi-Coder-AI while using HARMONIA-DSL internally.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phi_node import ΦπεNode, ΞΛΩStack, ΨΛΩLoop


class TestPhiPiEpsilonNode(unittest.TestCase):
    """Test ΦπεNode wrapper class"""
    
    def test_basic_initialization(self):
        """Test node can be initialized with parameters"""
        node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=0.1)
        self.assertEqual(node.ψ, 2.0)
        self.assertEqual(node.φ, 3.0)
        self.assertEqual(node.ε, 0.1)
    
    def test_stabilize_basic(self):
        """Test basic stabilization: (ψ + φ) * (1 - ε)"""
        node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=0.1)
        result = node.stabilize()
        expected = (2.0 + 3.0) * (1 - 0.1)  # 4.5
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_stabilize_zero_drift(self):
        """Test stabilization with zero drift"""
        node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=0.0)
        result = node.stabilize()
        expected = 2.0 + 3.0  # 5.0
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_stabilize_full_drift(self):
        """Test stabilization with full drift (ε=1)"""
        node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=1.0)
        result = node.stabilize()
        expected = 0.0  # (2 + 3) * 0 = 0
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_stabilize_negative_values(self):
        """Test stabilization with negative values"""
        node = ΦπεNode(ψ_signal=-1.0, φ_state=2.0, ε_drift=0.2)
        result = node.stabilize()
        expected = (-1.0 + 2.0) * (1 - 0.2)  # 0.8
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_stabilize_large_values(self):
        """Test stabilization with large values"""
        node = ΦπεNode(ψ_signal=1000.0, φ_state=2000.0, ε_drift=0.05)
        result = node.stabilize()
        expected = (1000.0 + 2000.0) * (1 - 0.05)  # 2850.0
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_update_psi(self):
        """Test updating psi signal"""
        node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=0.1)
        node.update(ψ_signal=5.0)
        self.assertEqual(node.ψ, 5.0)
        result = node.stabilize()
        expected = (5.0 + 3.0) * (1 - 0.1)  # 7.2
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_update_phi(self):
        """Test updating phi state"""
        node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=0.1)
        node.update(φ_state=7.0)
        self.assertEqual(node.φ, 7.0)
        result = node.stabilize()
        expected = (2.0 + 7.0) * (1 - 0.1)  # 8.1
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_update_epsilon(self):
        """Test updating epsilon drift"""
        node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=0.1)
        node.update(ε_drift=0.5)
        self.assertEqual(node.ε, 0.5)
        result = node.stabilize()
        expected = (2.0 + 3.0) * (1 - 0.5)  # 2.5
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_update_multiple(self):
        """Test updating multiple parameters at once"""
        node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=0.1)
        node.update(ψ_signal=4.0, φ_state=6.0, ε_drift=0.2)
        self.assertEqual(node.ψ, 4.0)
        self.assertEqual(node.φ, 6.0)
        self.assertEqual(node.ε, 0.2)
        result = node.stabilize()
        expected = (4.0 + 6.0) * (1 - 0.2)  # 8.0
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_get_state(self):
        """Test getting node state"""
        node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=0.1)
        node.stabilize()
        state = node.get_state()
        self.assertEqual(state['ψ'], 2.0)
        self.assertEqual(state['φ'], 3.0)
        self.assertEqual(state['ε'], 0.1)
        self.assertAlmostEqual(state['stabilized'], 4.5, places=5)
    
    def test_multiple_stabilizations(self):
        """Test multiple stabilizations with updates"""
        node = ΦπεNode(ψ_signal=1.0, φ_state=1.0, ε_drift=0.0)
        
        result1 = node.stabilize()
        self.assertAlmostEqual(result1, 2.0, places=5)
        
        node.update(ψ_signal=2.0)
        result2 = node.stabilize()
        self.assertAlmostEqual(result2, 3.0, places=5)
        
        node.update(ε_drift=0.5)
        result3 = node.stabilize()
        self.assertAlmostEqual(result3, 1.5, places=5)
    
    def test_repr(self):
        """Test string representation"""
        node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=0.1)
        repr_str = repr(node)
        self.assertIn("ΦπεNode", repr_str)
        self.assertIn("2.0", repr_str)
        self.assertIn("3.0", repr_str)
        self.assertIn("0.1", repr_str)


class TestXiLambdaOmegaStack(unittest.TestCase):
    """Test ΞΛΩStack wrapper class"""
    
    def test_initialization(self):
        """Test stack can be initialized"""
        stack = ΞΛΩStack()
        self.assertEqual(stack.size(), 0)
        self.assertTrue(stack.is_empty())
    
    def test_push_single(self):
        """Test pushing a single element"""
        stack = ΞΛΩStack()
        stack.push("A")
        self.assertEqual(stack.size(), 1)
        self.assertFalse(stack.is_empty())
        self.assertEqual(stack.peek(), "A")
    
    def test_push_multiple(self):
        """Test pushing multiple elements"""
        stack = ΞΛΩStack()
        stack.push("A")
        stack.push("B")
        stack.push("C")
        self.assertEqual(stack.size(), 3)
        self.assertEqual(stack.peek(), "C")
    
    def test_pop_single(self):
        """Test popping a single element"""
        stack = ΞΛΩStack()
        stack.push("A")
        popped = stack.pop()
        self.assertEqual(popped, "A")
        self.assertEqual(stack.size(), 0)
        self.assertTrue(stack.is_empty())
    
    def test_pop_multiple(self):
        """Test popping multiple elements"""
        stack = ΞΛΩStack()
        stack.push("A")
        stack.push("B")
        stack.push("C")
        
        self.assertEqual(stack.pop(), "C")
        self.assertEqual(stack.pop(), "B")
        self.assertEqual(stack.pop(), "A")
        self.assertTrue(stack.is_empty())
    
    def test_pop_empty(self):
        """Test popping from empty stack"""
        stack = ΞΛΩStack()
        result = stack.pop()
        self.assertIsNone(result)
    
    def test_peek_empty(self):
        """Test peeking at empty stack"""
        stack = ΞΛΩStack()
        result = stack.peek()
        self.assertIsNone(result)
    
    def test_harmonic_merge(self):
        """Test harmonic merge function"""
        stack = ΞΛΩStack()
        merged = stack.harmonic_merge("A", "B")
        self.assertEqual(merged, "[Ξ]A⟴B[Ω]")
    
    def test_recurse_two_elements(self):
        """Test recursion with two elements"""
        stack = ΞΛΩStack()
        stack.push("A")
        stack.push("B")
        stack.recurse()
        
        self.assertEqual(stack.size(), 1)
        result = stack.peek()
        # Stack pops B first (top), then A (bottom), so merge is B⟴A
        self.assertEqual(result, "[Ξ]B⟴A[Ω]")
    
    def test_recurse_three_elements(self):
        """Test recursion with three elements"""
        stack = ΞΛΩStack()
        stack.push("A")
        stack.push("B")
        stack.push("C")
        stack.recurse()
        
        self.assertEqual(stack.size(), 1)
        result = stack.peek()
        # Should merge B and C first, then merge with A
        self.assertIn("[Ξ]", result)
        self.assertIn("⟴", result)
        self.assertIn("[Ω]", result)
    
    def test_recurse_four_elements(self):
        """Test recursion with four elements"""
        stack = ΞΛΩStack()
        stack.push("A")
        stack.push("B")
        stack.push("C")
        stack.push("D")
        stack.recurse()
        
        self.assertEqual(stack.size(), 1)
        result = stack.peek()
        self.assertIn("[Ξ]", result)
        self.assertIn("[Ω]", result)
    
    def test_recurse_single_element(self):
        """Test recursion with single element (no-op)"""
        stack = ΞΛΩStack()
        stack.push("A")
        stack.recurse()
        
        self.assertEqual(stack.size(), 1)
        self.assertEqual(stack.peek(), "A")
    
    def test_recurse_empty(self):
        """Test recursion with empty stack (no-op)"""
        stack = ΞΛΩStack()
        stack.recurse()
        self.assertEqual(stack.size(), 0)
    
    def test_clear(self):
        """Test clearing the stack"""
        stack = ΞΛΩStack()
        stack.push("A")
        stack.push("B")
        stack.push("C")
        stack.clear()
        
        self.assertEqual(stack.size(), 0)
        self.assertTrue(stack.is_empty())
    
    def test_repr(self):
        """Test string representation"""
        stack = ΞΛΩStack()
        stack.push("A")
        stack.push("B")
        repr_str = repr(stack)
        self.assertIn("ΞΛΩStack", repr_str)
        self.assertIn("2", repr_str)


class TestPsiLambdaOmegaLoop(unittest.TestCase):
    """Test ΨΛΩLoop wrapper class"""
    
    def test_initialization(self):
        """Test loop can be initialized"""
        loop = ΨΛΩLoop()
        self.assertEqual(loop.get_output(), 0.0)
    
    def test_iterate_once(self):
        """Test single iteration"""
        loop = ΨΛΩLoop()
        result = loop.iterate(10.0)
        # output = (0 * 0.618) + (10 * 0.382) = 3.82
        expected = 10.0 * (1 - loop.PHI)
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_iterate_twice(self):
        """Test two iterations"""
        loop = ΨΛΩLoop()
        result1 = loop.iterate(10.0)
        result2 = loop.iterate(5.0)
        
        # First: (0 * 0.618) + (10 * 0.382) = 3.82
        # Second: (3.82 * 0.618) + (5 * 0.382) = 4.27
        expected1 = 10.0 * (1 - loop.PHI)
        expected2 = (expected1 * loop.PHI) + (5.0 * (1 - loop.PHI))
        
        self.assertAlmostEqual(result1, expected1, places=2)
        self.assertAlmostEqual(result2, expected2, places=2)
    
    def test_iterate_convergence(self):
        """Test that loop converges with constant input"""
        loop = ΨΛΩLoop()
        
        # Iterate 10 times with constant input
        for _ in range(10):
            result = loop.iterate(10.0)
        
        # Should converge toward input value
        self.assertGreater(result, 8.0)  # Close to 10
        self.assertLess(result, 10.0)    # But not exactly 10
    
    def test_iterate_zero_input(self):
        """Test iteration with zero input"""
        loop = ΨΛΩLoop()
        loop.iterate(10.0)  # Set non-zero output
        result = loop.iterate(0.0)
        
        # Should dampen toward zero
        self.assertGreater(result, 0.0)
        self.assertLess(result, 10.0)
    
    def test_iterate_negative_input(self):
        """Test iteration with negative input"""
        loop = ΨΛΩLoop()
        result = loop.iterate(-5.0)
        
        # Should handle negative values
        self.assertLess(result, 0.0)
    
    def test_reset(self):
        """Test resetting the loop"""
        loop = ΨΛΩLoop()
        loop.iterate(10.0)
        loop.iterate(5.0)
        
        self.assertNotEqual(loop.get_output(), 0.0)
        
        loop.reset()
        self.assertEqual(loop.get_output(), 0.0)
    
    def test_get_output(self):
        """Test getting output value"""
        loop = ΨΛΩLoop()
        self.assertEqual(loop.get_output(), 0.0)
        
        loop.iterate(10.0)
        output = loop.get_output()
        self.assertGreater(output, 0.0)
    
    def test_golden_ratio_constant(self):
        """Test that PHI is the golden ratio"""
        loop = ΨΛΩLoop()
        # Golden ratio: (√5 - 1) / 2 ≈ 0.618033988749895
        self.assertAlmostEqual(loop.PHI, 0.618033988749895, places=10)
    
    def test_repr(self):
        """Test string representation"""
        loop = ΨΛΩLoop()
        loop.iterate(10.0)
        repr_str = repr(loop)
        self.assertIn("ΨΛΩLoop", repr_str)
        self.assertIn("output", repr_str)


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility with Phi-Coder-AI"""
    
    def test_phi_coder_ai_example_1(self):
        """Test example from Phi-Coder-AI documentation"""
        # Original Phi-Coder-AI code:
        # node = ΦπεNode(2.0, 3.0, 0.1)
        # result = node.stabilize()
        
        node = ΦπεNode(ψ_signal=2.0, φ_state=3.0, ε_drift=0.1)
        result = node.stabilize()
        self.assertAlmostEqual(result, 4.5, places=5)
    
    def test_phi_coder_ai_example_2(self):
        """Test stack example from Phi-Coder-AI"""
        # Original Phi-Coder-AI code:
        # stack = ΞΛΩStack()
        # stack.push("A")
        # stack.push("B")
        # stack.recurse()
        
        stack = ΞΛΩStack()
        stack.push("A")
        stack.push("B")
        stack.recurse()
        
        result = stack.peek()
        # Stack pops B first (top), then A (bottom), so merge is B⟴A
        self.assertEqual(result, "[Ξ]B⟴A[Ω]")
    
    def test_phi_coder_ai_example_3(self):
        """Test loop example from Phi-Coder-AI"""
        # Original Phi-Coder-AI code:
        # loop = ΨΛΩLoop()
        # result = loop.iterate(10.0)
        
        loop = ΨΛΩLoop()
        result = loop.iterate(10.0)
        
        # Should match Phi-Coder-AI behavior
        expected = 10.0 * 0.382  # 3.82
        self.assertAlmostEqual(result, expected, places=2)


if __name__ == '__main__':
    unittest.main()
