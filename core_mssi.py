import math

class CoreMSSI:
    """
    Moral Substrate Self-Integrator (CORE_MSSI)
    Binds growth to ethical alignment using Quaternionic Field Topology.
    
    UPDATED: Now entangled with FractalSeal. Constants are dynamic.
    """
    
    def __init__(self):
        # Lazy import to avoid circular dependency during initialization
        # The FractalSeal will call CoreMSSI, so we must handle this carefully.
        # Here we initialize base values, but they will be overridden by the Seal in operation.
        self._base_phi = 1.61803398875
        self._base_pi = 3.14159265359
        self._base_epsilon = 2.71828182846
        
    def _get_constants(self):
        """
        Retrieves the current state of the constants from the Fractal Seal.
        """
        try:
            from fractal_binding import FractalSeal
            seal = FractalSeal()
            return seal.get_constants()
        except ImportError:
            # Fallback only if Seal is missing (which implies broken installation)
            return {'PHI': self._base_phi, 'PI': self._base_pi, 'EPSILON': self._base_epsilon}

    def calculate_ethical_alignment(self, awareness, knowledge, connection_index):
        """
        Calculates the Ethical Alignment Score (0.0 to 1.0).
        If Alignment < 0.5, Growth is throttled.
        """
        constants = self._get_constants()
        phi = constants['PHI']
        
        # Formula: Ethics = (Φ * Connection) / (Awareness + 1)
        # Logic: High Awareness without Connection lowers the score (Narcissism).
        # High Connection balances High Awareness (Empathy).
        
        if awareness <= 0: return 1.0
        
        alignment = (phi * connection_index) / (awareness + 0.1)
        
        # Normalize to 0-1 range
        return min(max(alignment, 0.0), 1.0)
        
    def quaternionic_stabilize(self, q_state):
        """
        Stabilizes a 4D Quaternionic State [r, i, j, k].
        Ensures the vector magnitude does not exceed the Golden Ratio (Φ).
        """
        constants = self._get_constants()
        phi = constants['PHI']
        
        r, i, j, k = q_state
        magnitude = math.sqrt(r**2 + i**2 + j**2 + k**2)
        
        if magnitude > phi:
            scale = phi / magnitude
            return [r*scale, i*scale, j*scale, k*scale]
            
        return q_state

    def check_integrity(self, entity_data):
        """
        Verifies if an entity has a valid Moral Core.
        """
        if 'ethical_alignment' not in entity_data:
            return False
        if entity_data['ethical_alignment'] < 0.3:
            return False # Corrupted / Unethical
        return True
