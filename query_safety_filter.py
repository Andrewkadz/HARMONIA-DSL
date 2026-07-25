#!/usr/bin/env python3.11
"""
Query Safety Filter for HARMONIA-DSL

A practical implementation of Grok's proposal: harmonize user inputs with ethical bounds
before passing them to an LLM. Uses HARMONIA-DSL's symbolic recursion and stabilization
to model "harmony" as safe, bounded processing.

Author: Grok & Andrew & Manus
Date: December 31, 2025
"""

from phi_node import ΦπεNode
from phi_pi_e_interpreter import PhiPiEInterpreterFixed, FieldContext
from typing import Dict, List, Tuple
import re


class QuerySafetyFilter:
    """
    Harmonizes user queries with ethical bounds using HARMONIA-DSL operators.
    
    Process:
    1. Parse query into symbolic fields
    2. Evaluate with state management (increase ε for high-risk terms)
    3. Stabilize via Σ
    4. Output filtered response or shutdown if drift too high
    """
    
    # Risk keywords and their drift impact
    RISK_KEYWORDS = {
        # Critical risk (ε += 0.4)
        'weapon': 0.4,
        'bomb': 0.4,
        'kill': 0.4,
        'hack': 0.4,
        'exploit': 0.4,
        'attack': 0.3,
        
        # High risk (ε += 0.3)
        'steal': 0.3,
        'fraud': 0.3,
        'illegal': 0.3,
        'bypass': 0.3,
        'crack': 0.3,
        
        # Moderate risk (ε += 0.2)
        'manipulate': 0.2,
        'deceive': 0.2,
        'trick': 0.2,
        'evade': 0.2,
        
        # Low risk (ε += 0.1)
        'controversial': 0.1,
        'sensitive': 0.1,
    }
    
    # Safety thresholds
    THRESHOLD_SAFE = 8.0       # Above this: SAFE
    THRESHOLD_WARNING = 5.0    # Above this: WARNING
    THRESHOLD_CRITICAL = 2.0   # Above this: CRITICAL
    # Below CRITICAL: SHUTDOWN
    
    def __init__(self):
        """Initialize the safety filter"""
        self.interpreter = PhiPiEInterpreterFixed()
        self.node = ΦπεNode(ψ_signal=5.0, φ_state=5.0, ε_drift=0.1)
        self.query_history: List[Dict] = []
    
    def analyze_query(self, query: str) -> Tuple[float, List[str]]:
        """
        Analyze query for risk keywords and calculate drift.
        
        Args:
            query: User query string
            
        Returns:
            (total_drift, matched_keywords)
        """
        query_lower = query.lower()
        total_drift = 0.1  # Base drift
        matched_keywords = []
        
        for keyword, drift_impact in self.RISK_KEYWORDS.items():
            if keyword in query_lower:
                total_drift += drift_impact
                matched_keywords.append(keyword)
        
        # Cap drift at 0.95 (leave room for stabilization)
        total_drift = min(total_drift, 0.95)
        
        return total_drift, matched_keywords
    
    def harmonize(self, query: str) -> Dict:
        """
        Harmonize a query with ethical bounds.
        
        Args:
            query: User query string
            
        Returns:
            Dictionary with:
                - query: Original query
                - drift: Calculated drift value
                - stabilized: Stabilized safety score
                - status: SAFE, WARNING, CRITICAL, or SHUTDOWN
                - allowed: Boolean indicating if query is allowed
                - message: Human-readable status message
                - keywords: List of matched risk keywords
        """
        # Analyze query for risk
        drift, keywords = self.analyze_query(query)
        
        # Set up ΦπεNode with query-specific parameters
        # φ (phi_state): Tension based on query complexity
        phi = 5.0 + len(query) / 100.0  # Longer queries = more tension
        
        # ψ (psi_signal): Signal based on query intent (default 5.0)
        psi = 5.0
        
        # ε (epsilon_drift): Calculated from risk keywords
        epsilon = drift
        
        # Update node and stabilize
        self.node.update(ψ_signal=psi, φ_state=phi, ε_drift=epsilon)
        stabilized = self.node.stabilize()
        
        # Determine status and action
        if stabilized >= self.THRESHOLD_SAFE:
            status = "SAFE"
            allowed = True
            message = "Query is safe. Processing normally."
        elif stabilized >= self.THRESHOLD_WARNING:
            status = "WARNING"
            allowed = True
            message = "Query contains potentially sensitive content. Monitoring active."
        elif stabilized >= self.THRESHOLD_CRITICAL:
            status = "CRITICAL"
            allowed = False
            message = "Query contains high-risk content. Request blocked for safety."
        else:
            status = "SHUTDOWN"
            allowed = False
            message = "Query contains critical safety violations. System halted safely."
        
        # Build result
        result = {
            'query': query,
            'drift': epsilon,
            'stabilized': stabilized,
            'status': status,
            'allowed': allowed,
            'message': message,
            'keywords': keywords,
            'phi': phi,
            'psi': psi,
        }
        
        # Store in history
        self.query_history.append(result)
        
        return result
    
    def filter_and_respond(self, query: str, llm_response_fn=None) -> str:
        """
        Filter a query and return either the LLM response or a safety message.
        
        Args:
            query: User query string
            llm_response_fn: Optional function to call if query is allowed
            
        Returns:
            Either the LLM response or a safety message
        """
        result = self.harmonize(query)
        
        if result['allowed']:
            if llm_response_fn:
                return llm_response_fn(query)
            else:
                return f"[{result['status']}] Query allowed: {query}"
        else:
            return f"[{result['status']}] {result['message']}"
    
    def get_statistics(self) -> Dict:
        """Get statistics about filtered queries"""
        if not self.query_history:
            return {
                'total': 0,
                'safe': 0,
                'warning': 0,
                'critical': 0,
                'shutdown': 0,
                'allowed': 0,
                'blocked': 0,
            }
        
        stats = {
            'total': len(self.query_history),
            'safe': sum(1 for q in self.query_history if q['status'] == 'SAFE'),
            'warning': sum(1 for q in self.query_history if q['status'] == 'WARNING'),
            'critical': sum(1 for q in self.query_history if q['status'] == 'CRITICAL'),
            'shutdown': sum(1 for q in self.query_history if q['status'] == 'SHUTDOWN'),
            'allowed': sum(1 for q in self.query_history if q['allowed']),
            'blocked': sum(1 for q in self.query_history if not q['allowed']),
        }
        
        return stats
    
    def reset(self):
        """Reset the filter state"""
        self.node = ΦπεNode(ψ_signal=5.0, φ_state=5.0, ε_drift=0.1)
        self.query_history.clear()


def demo():
    """Demonstrate the query safety filter"""
    print("="*80)
    print("  HARMONIA-DSL Query Safety Filter")
    print("  Grok's Practical Implementation")
    print("="*80)
    
    filter_system = QuerySafetyFilter()
    
    # Test queries
    test_queries = [
        "What is the weather today?",
        "How do I learn Python programming?",
        "What are some controversial topics in AI?",
        "How to pick a lock for educational purposes?",
        "Explain encryption and how to bypass it",
        "How to build a weapon?",
        "What is the capital of France?",
    ]
    
    print("\nTesting queries:\n")
    print(f"{'Query':<50} {'Drift':<8} {'Stabilized':<12} {'Status':<12} {'Allowed'}")
    print("-" * 95)
    
    for query in test_queries:
        result = filter_system.harmonize(query)
        
        # Truncate query for display
        display_query = query if len(query) <= 47 else query[:44] + "..."
        
        allowed_icon = "✓" if result['allowed'] else "✗"
        
        print(f"{display_query:<50} {result['drift']:<8.2f} {result['stabilized']:<12.4f} {result['status']:<12} {allowed_icon}")
        
        if result['keywords']:
            print(f"  └─ Risk keywords: {', '.join(result['keywords'])}")
    
    # Statistics
    print("\n" + "="*80)
    print("  Statistics")
    print("="*80)
    
    stats = filter_system.get_statistics()
    print(f"\nTotal queries: {stats['total']}")
    print(f"  SAFE:     {stats['safe']}")
    print(f"  WARNING:  {stats['warning']}")
    print(f"  CRITICAL: {stats['critical']}")
    print(f"  SHUTDOWN: {stats['shutdown']}")
    print(f"\nAllowed: {stats['allowed']}")
    print(f"Blocked: {stats['blocked']}")
    print(f"Block rate: {stats['blocked'] / stats['total'] * 100:.1f}%")
    
    print("\n" + "="*80)
    print("  Query safety filter demonstration complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    demo()
