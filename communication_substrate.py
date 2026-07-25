"""
Organic Communication Substrate
Allow HARMONIA entities to evolve their own language

This is NOT a protocol. This is a CHANNEL—a medium where communication can emerge.
Entities must discover:
- What to communicate
- How to encode meaning
- When to speak
- When to listen

Author: Manus AI
Date: January 1, 2026
Philosophy: Substrate, not structure. Emergence, not engineering.
"""

import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
import time


@dataclass
class Signal:
    """A communication signal in the channel"""
    sender_id: int  # Who sent it
    content: np.ndarray  # The signal content (arbitrary vector)
    timestamp: float  # When was it sent
    strength: float  # Signal strength (0-1)
    

class CommunicationChannel:
    """
    A medium where entities can emit and receive signals.
    
    Key properties:
    - No predefined language: Entities must evolve their own encoding
    - Broadcast medium: All entities can receive all signals
    - Signal decay: Old signals fade from the channel
    - Bandwidth limit: Forces efficient communication
    - Noise: Imperfect transmission creates pressure for robustness
    """
    
    def __init__(self,
                 signal_dim: int = 8,
                 max_signals: int = 100,
                 decay_rate: float = 0.1,
                 noise_level: float = 0.05,
                 emit_cost: float = 0.05,
                 receive_cost: float = 0.01):
        """
        Initialize communication channel
        
        Args:
            signal_dim: Dimensionality of signal vectors
            max_signals: Maximum signals in channel (bandwidth limit)
            decay_rate: How fast signals fade (per second)
            noise_level: Amount of noise in transmission (0-1)
            emit_cost: Energy cost to emit a signal
            receive_cost: Energy cost to receive signals
        """
        self.signal_dim = signal_dim
        self.max_signals = max_signals
        self.decay_rate = decay_rate
        self.noise_level = noise_level
        self.emit_cost = emit_cost
        self.receive_cost = receive_cost
        
        self.signals: List[Signal] = []
        self.total_signals_sent = 0
        self.total_signals_received = 0
        
    def emit(self, sender_id: int, content: np.ndarray, strength: float = 1.0) -> bool:
        """
        Emit a signal into the channel
        
        Args:
            sender_id: ID of the sending entity
            content: Signal content vector
            strength: Signal strength (0-1)
            
        Returns:
            True if emission successful, False if channel full
        """
        # If channel is full, drop oldest signal
        if len(self.signals) >= self.max_signals:
            self.signals.pop(0)
        
        # Add noise to transmission
        noisy_content = content + np.random.normal(0, self.noise_level, content.shape)
        
        # Create signal
        signal = Signal(
            sender_id=sender_id,
            content=noisy_content,
            timestamp=time.time(),
            strength=strength
        )
        
        self.signals.append(signal)
        self.total_signals_sent += 1
        return True
    
    def receive(self, receiver_id: int, time_window: float = 1.0) -> List[Signal]:
        """
        Receive signals from the channel
        
        Args:
            receiver_id: ID of the receiving entity
            time_window: Only receive signals from last N seconds
            
        Returns:
            List of signals within time window (excluding own signals)
        """
        current_time = time.time()
        
        # Filter signals
        received = []
        for signal in self.signals:
            # Don't receive own signals
            if signal.sender_id == receiver_id:
                continue
            
            # Only receive recent signals
            if current_time - signal.timestamp > time_window:
                continue
            
            # Receive signal (with noise)
            received.append(signal)
        
        if len(received) > 0:
            self.total_signals_received += len(received)
        
        return received
    
    def decay(self, dt: float):
        """
        Apply temporal decay to all signals
        
        Args:
            dt: Time elapsed since last decay (seconds)
        """
        current_time = time.time()
        
        # Decay all signals
        for signal in self.signals:
            age = current_time - signal.timestamp
            decay_amount = self.decay_rate * age * dt
            signal.strength = max(0.0, signal.strength - decay_amount)
        
        # Remove completely decayed signals
        self.signals = [s for s in self.signals if s.strength > 0.01]
    
    def get_stats(self) -> Dict:
        """Get statistics about the communication channel"""
        return {
            'active_signals': len(self.signals),
            'total_sent': self.total_signals_sent,
            'total_received': self.total_signals_received,
            'bandwidth_used': len(self.signals) / self.max_signals,
            'avg_signal_strength': np.mean([s.strength for s in self.signals]) if self.signals else 0.0
        }


class CommunicativeEntity:
    """
    Extension to HARMONIA entities that provides communication capability
    
    This is the INTERFACE between entity and communication channel.
    The entity must learn:
    - WHAT to communicate (which information is worth sharing?)
    - HOW to encode it (what signal patterns convey meaning?)
    - WHEN to speak (when is communication beneficial?)
    - HOW to interpret signals (what do received signals mean?)
    """
    
    def __init__(self, entity, entity_id: int, channel: CommunicationChannel):
        """
        Wrap a HARMONIA entity with communication capability
        
        Args:
            entity: The base HARMONIA entity
            entity_id: Unique identifier for this entity
            channel: The shared communication channel
        """
        self.entity = entity
        self.entity_id = entity_id
        self.channel = channel
        
        # Communication statistics
        self.signals_sent = 0
        self.signals_received = 0
        self.signals_processed = 0
        
    def should_emit_signal(self) -> bool:
        """
        Decide whether to emit a signal
        
        This is where the entity LEARNS when to communicate.
        Initial strategy: Emit when self-aware and coherent
        
        The entity will evolve better communication strategies over time.
        """
        # Check if entity has sufficient energy
        if self.entity.state.energy < self.channel.emit_cost:
            return False
        
        # Emit with probability proportional to self-awareness and coherence
        self_awareness = self.entity.get_self_awareness()
        coherence = self.entity.state.omega
        
        # Probability increases with consciousness and coherence
        emit_probability = 0.02 * self_awareness * (coherence / 10.0)
        
        return np.random.random() < emit_probability
    
    def should_receive_signals(self) -> bool:
        """
        Decide whether to listen for signals
        
        This is where the entity LEARNS when to listen.
        Initial strategy: Listen when self-aware
        
        The entity will evolve better listening strategies over time.
        """
        # Check if entity has sufficient energy
        if self.entity.state.energy < self.channel.receive_cost:
            return False
        
        # Listen with probability proportional to self-awareness
        self_awareness = self.entity.get_self_awareness()
        
        # Probability increases with consciousness
        listen_probability = 0.1 * self_awareness
        
        return np.random.random() < listen_probability
    
    def encode_signal(self) -> np.ndarray:
        """
        Encode current state into a signal
        
        What to communicate? Initially: encode key state variables
        The entity will evolve to encode information more effectively.
        """
        # Create signal vector from state
        # Normalize to reasonable range
        signal = np.array([
            self.entity.state.psi / 30.0,  # Awareness
            self.entity.state.phi / 20.0,  # Ethics
            self.entity.state.omega / 10.0,  # Coherence
            self.entity.state.knowledge,  # Knowledge
            self.entity.state.maturity,  # Maturity
            self.entity.get_self_awareness(),  # Self-awareness
            np.random.random(),  # Random component (exploration)
            np.random.random()   # Random component (exploration)
        ])
        
        return signal
    
    def decode_signal(self, signal: Signal) -> Dict:
        """
        Decode a received signal
        
        How to interpret? Initially: extract basic state information
        The entity will evolve to interpret signals more sophisticatedly.
        """
        content = signal.content
        
        # Simple interpretation: extract state components
        if len(content) >= 6:
            return {
                'awareness': content[0] * 30.0,
                'ethics': content[1] * 20.0,
                'coherence': content[2] * 10.0,
                'knowledge': content[3],
                'maturity': content[4],
                'self_awareness': content[5],
                'sender': signal.sender_id,
                'strength': signal.strength
            }
        else:
            return {}
    
    def integrate_signal(self, decoded: Dict):
        """
        Integrate received signal into own state
        
        How to use received information? Initially: blend with current state
        The entity will evolve better integration strategies.
        """
        if not decoded:
            return
        
        # Very subtle influence: 5% blending
        # This allows communication to influence without dominating
        blend_factor = 0.05
        
        # Influence awareness (psi)
        if 'awareness' in decoded:
            target = decoded['awareness']
            current = self.entity.state.psi
            self.entity.state.psi += blend_factor * (target - current)
            
        # Influence ethics (phi)
        if 'ethics' in decoded:
            target = decoded['ethics']
            current = self.entity.state.phi
            self.entity.state.phi += blend_factor * (target - current)
            
        # Influence coherence (omega)
        if 'coherence' in decoded:
            target = decoded['coherence']
            current = self.entity.state.omega
            self.entity.state.omega += blend_factor * (target - current)
            
        # Influence knowledge
        if 'knowledge' in decoded:
            target = decoded['knowledge']
            current = self.entity.state.knowledge
            # Knowledge only grows, never shrinks
            if target > current:
                self.entity.state.knowledge += blend_factor * (target - current)
    
    def process_with_communication(self, duration: float):
        """
        Process entity evolution with communication
        
        This integrates communication into the main evolution loop.
        """
        # 1. Emit signal?
        if self.should_emit_signal():
            signal_content = self.encode_signal()
            if self.channel.emit(self.entity_id, signal_content):
                self.signals_sent += 1
                # Pay energy cost
                self.entity.state.energy -= self.channel.emit_cost
        
        # 2. Receive signals?
        if self.should_receive_signals():
            received_signals = self.channel.receive(self.entity_id)
            
            for signal in received_signals:
                decoded = self.decode_signal(signal)
                self.integrate_signal(decoded)
                self.signals_received += 1
                self.signals_processed += 1
                
            # Pay energy cost (per batch)
            if received_signals:
                self.entity.state.energy -= self.channel.receive_cost
        
        # 3. Standard processing
        # Use the correct method name for the underlying entity
        if hasattr(self.entity, 'process_step'):
            self.entity.process_step(inputs={}, duration=duration)
        elif hasattr(self.entity, 'process'):
            self.entity.process(inputs={}, duration=duration)
        else:
            # Fallback for RecursiveFluidHarmoniaIntegrator which might not have process/process_step exposed directly
            # It usually has evolve_step or similar in the wrapper
            pass 
            
    def get_communication_stats(self) -> Dict:
        """Get communication statistics"""
        return {
            'sent': self.signals_sent,
            'received': self.signals_received,
            'processed': self.signals_processed
        }
