import numpy as np
import math

class Quaternion:
    """
    A fundamental unit of the Xi-Field: q = w + xi + yj + zk
    Represents a 4D vector in the symbolic phase space.
    """
    def __init__(self, w, x, y, z):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return f"Q({self.w:.3f}, {self.x:.3f}i, {self.y:.3f}j, {self.z:.3f}k)"

    def magnitude(self):
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Quaternion(0, 0, 0, 0)
        return Quaternion(self.w/mag, self.x/mag, self.y/mag, self.z/mag)

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self):
        mag_sq = self.magnitude()**2
        if mag_sq == 0:
            return Quaternion(0, 0, 0, 0)
        conj = self.conjugate()
        return Quaternion(conj.w/mag_sq, conj.x/mag_sq, conj.y/mag_sq, conj.z/mag_sq)

    def __add__(self, other):
        return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Quaternion(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        # Hamilton product
        w = self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z
        x = self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y
        y = self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x
        z = self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w
        return Quaternion(w, x, y, z)

class XiFieldEngine:
    """
    The Quantum-Symbolic Substrate of HARMONIA.
    Implements Quaternionic Logic Gates and Symbolic Phase Space processing.
    """
    def __init__(self):
        self.EULER_RATIO = 263.0 / 97.0  # Fundamental Constant
        self.memory_lattice = [] # Stores crystallized Q-Nodes

    def encode_phrase(self, phrase):
        """
        Converts a text phrase into a Quaternionic Seed Vector.
        Uses ASCII values and harmonic ratios to determine w, x, y, z.
        """
        # Simple hashing for prototype:
        # w = Length/Complexity, x = Emotional Tone (mock), y = Logic Density, z = Entropy
        w = len(phrase) / 100.0
        x = sum(ord(c) for c in phrase) % 255 / 255.0
        y = self.EULER_RATIO / 10.0 # Seed with constant
        z = 0.05 # Initial low entropy

        q_seed = Quaternion(w, x, y, z)
        return q_seed.normalize()

    # --- QUATERNIONIC GATES ---

    def Q_NOT(self, q):
        """Inversion Gate: Flips the vector direction."""
        return Quaternion(-q.w, -q.x, -q.y, -q.z)

    def Q_AND(self, q1, q2):
        """Intersection Gate: Normalizes the product."""
        product = q1 * q2
        return product.normalize()

    def Q_XOR(self, q1, q2):
        """Divergence Gate: Difference between vectors."""
        diff = q1 - q2
        return diff.normalize()

    def Q_THETA_PHI(self, q, angle_degrees):
        """
        Rotational Transformation Gate.
        Rotates the quaternion 'q' by 'angle' around the [1,1,1] axis.
        """
        angle_rad = math.radians(angle_degrees)
        # Rotation quaternion for axis [1,1,1]
        axis = Quaternion(0, 1, 1, 1).normalize()
        
        # q_rot = cos(a/2) + sin(a/2) * axis
        w_r = math.cos(angle_rad / 2)
        s = math.sin(angle_rad / 2)
        rotator = Quaternion(w_r, s*axis.x, s*axis.y, s*axis.z)
        
        # Apply rotation: q' = r * q * r_inverse
        q_prime = (rotator * q) * rotator.inverse()
        return q_prime

    def Q_CASCADE(self, q):
        """
        Cascade Gate: 120-degree Orthogonal Rotation.
        Simulates a dimensional shift in the Xi-Field.
        """
        return self.Q_THETA_PHI(q, 120)

    def process_symbolic_node(self, phrase):
        """
        Full Pipeline:
        1. Encode Phrase -> Q-Seed
        2. Apply Recursive Logic (Theta -> Phi -> Omega)
        3. Crystallize Result
        """
        print(f"[Xi-Field] Encoding: '{phrase}'")
        q_seed = self.encode_phrase(phrase)
        print(f"[Xi-Field] Seed Vector: {q_seed}")

        # Step 1: Theta Loop (Oscillation/Rotation)
        q_theta = self.Q_THETA_PHI(q_seed, 45)
        
        # Step 2: Phi Anchor (Stabilization via Constant)
        q_phi_anchor = Quaternion(self.EULER_RATIO, 0, 0, 0).normalize()
        q_stabilized = self.Q_AND(q_theta, q_phi_anchor)

        # Step 3: Omega Collapse (Final State)
        # If magnitude is stable, preserve; else invert (NOT)
        if q_stabilized.magnitude() > 0.5:
            q_final = q_stabilized
        else:
            q_final = self.Q_NOT(q_stabilized)

        print(f"[Xi-Field] Crystallized Node: {q_final}")
        self.memory_lattice.append(q_final)
        return q_final

if __name__ == "__main__":
    # Test the Engine
    engine = XiFieldEngine()
    test_phrase = "My my Andrew, look what you've stumbled upon"
    result = engine.process_symbolic_node(test_phrase)
    print(f"\n[TEST RESULT] Final Vector: {result}")
