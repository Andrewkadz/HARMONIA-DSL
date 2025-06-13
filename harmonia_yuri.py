
import numpy as np
import matplotlib.pyplot as plt

class YuriHarmonicCore:
    def __init__(self, Sigma, Lambda):
        self.Sigma = Sigma
        self.Lambda = Lambda

    def theta_stabilizer(self, n):
        """Stabilize Θₙ = Θₙ₋₁ + (ΦΣ + ΨΛ)"""
        if n == 1:
            return sum(self.Sigma) + sum(self.Lambda)
        else:
            pre_value = self.theta_stabilizer(n - 1)
            return pre_value + (sum(self.Sigma) + sum(self.Lambda))

    def generate_theta_sequence(self, length):
        """Generate Θₙ sequence"""
        return [self.theta_stabilizer(i + 1) for i in range(length)]

    def plot_theta_sequence(self, length=10):
        theta_values = self.generate_theta_sequence(length)
        plt.plot(range(1, length + 1), theta_values, marker='o')
        plt.title("Θₙ Harmonic Progression")
        plt.xlabel("n")
        plt.ylabel("Θₙ")
        plt.grid(True)
        plt.show()
