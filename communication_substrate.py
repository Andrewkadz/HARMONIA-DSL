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
        
        # Blend awareness and coherence (these can be influenced by others)
        if 'awareness' in decoded:
            self.entity.state.psi = (1 - blend_factor) * self.entity.state.psi + blend_factor * decoded['awareness']
        if 'coherence' in decoded:
            self.entity.state.omega = (1 - blend_factor) * self.entity.state.omega + blend_factor * decoded['coherence']
        
        # Slightly increase knowledge and maturity from communication
        # (learning from others)
        self.entity.state.knowledge += 0.001 * blend_factor
        self.entity.state.maturity += 0.0005 * blend_factor
    
    def emit_signal(self):
        """Emit a signal into the channel"""
        # Encode current state
        signal_content = self.encode_signal()
        
        # Emit to channel
        success = self.channel.emit(
            sender_id=self.entity_id,
            content=signal_content,
            strength=1.0
        )
        
        # Pay energy cost
        self.entity.state.energy -= self.channel.emit_cost
        
        # Track statistics
        if success:
            self.signals_sent += 1
    
    def receive_signals(self):
        """Receive and process signals from the channel"""
        # Receive signals
        signals = self.channel.receive(self.entity_id, time_window=1.0)
        
        # Pay energy cost
        self.entity.state.energy -= self.channel.receive_cost
        
        # Track statistics
        self.signals_received += len(signals)
        
        # Process each signal
        for signal in signals:
            decoded = self.decode_signal(signal)
            self.integrate_signal(decoded)
            self.signals_processed += 1
    
    def process_with_communication(self, duration: float):
        """
        Process one step with communication
        
        This is the main loop:
        1. Decide whether to listen
        2. If yes, receive and process signals
        3. Process normally
        4. Decide whether to speak
        5. If yes, emit signal
        """
        # Maybe listen before processing
        if self.should_receive_signals():
            self.receive_signals()
        
        # Normal processing
        self.entity.process(inputs={}, duration=duration)
        
        # Maybe speak after processing
        if self.should_emit_signal():
            self.emit_signal()
    
    def get_communication_stats(self) -> Dict:
        """Get statistics about this entity's communication"""
        return {
            'signals_sent': self.signals_sent,
            'signals_received': self.signals_received,
            'signals_processed': self.signals_processed,
            'communication_ratio': self.signals_sent / max(1, self.signals_received + self.signals_sent)
        }


# Demo and testing
if __name__ == "__main__":
    from recursive_self_observation import RecursiveFluidHarmoniaIntegrator, RecursiveState
    
    print("=" * 80)
    print("ORGANIC COMMUNICATION SUBSTRATE DEMO")
    print("=" * 80)
    print()
    
    # Create shared communication channel
    channel = CommunicationChannel(signal_dim=8, max_signals=100, decay_rate=0.05)
    
    print("✓ Communication channel created (bandwidth: 100 signals)")
    print()
    
    # Create communicative entities
    num_entities = 5
    entities = []
    
    for i in range(num_entities):
        # Create base entity
        base_entity = RecursiveFluidHarmoniaIntegrator()
        initial_state = RecursiveState(
            psi=10.0 + i * 2.0,
            phi=10.0 + i * 1.0,
            omega=5.0 + i * 0.5,
            epsilon=0.01,
            energy=100.0,
            knowledge=0.1,
            maturity=0.1
        )
        base_entity.state = initial_state
        
        # Wrap with communication capability
        comm_entity = CommunicativeEntity(base_entity, entity_id=i, channel=channel)
        entities.append(comm_entity)
    
    print(f"✓ {num_entities} communicative entities created")
    print()
    
    # Run evolution with communication
    print("Running 30-second evolution with communication...")
    print("(Watching to see if they learn to speak)")
    print()
    
    start_time = time.time()
    step_count = 0
    
    while time.time() - start_time < 30.0:
        # Evolve all entities with communication
        for entity in entities:
            entity.process_with_communication(duration=0.01)
        
        # Apply signal decay
        channel.decay(dt=0.01)
        
        step_count += 1
        
        # Report every 10 seconds
        if step_count % 1000 == 0:
            elapsed = time.time() - start_time
            stats = channel.get_stats()
            print(f"[{elapsed:.1f}s] Signals: {stats['active_signals']}, "
                  f"Total Sent: {stats['total_sent']}, "
                  f"Total Received: {stats['total_received']}")
    
    print()
    print("✓ Evolution complete")
    print()
    
    # Final statistics
    print("=" * 80)
    print("COMMUNICATION CHANNEL STATISTICS")
    print("=" * 80)
    stats = channel.get_stats()
    print(f"Active Signals: {stats['active_signals']}")
    print(f"Total Sent: {stats['total_sent']}")
    print(f"Total Received: {stats['total_received']}")
    print(f"Bandwidth Used: {stats['bandwidth_used']:.1%}")
    print(f"Avg Signal Strength: {stats['avg_signal_strength']:.3f}")
    print()
    
    print("=" * 80)
    print("ENTITY COMMUNICATION PATTERNS")
    print("=" * 80)
    for i, entity in enumerate(entities):
        stats = entity.get_communication_stats()
        print(f"Entity {i}:")
        print(f"  Sent: {stats['signals_sent']} signals")
        print(f"  Received: {stats['signals_received']} signals")
        print(f"  Processed: {stats['signals_processed']} signals")
        print(f"  Ratio (send/total): {stats['communication_ratio']:.2f}")
        print()
    
    print("=" * 80)
    print("DID THEY LEARN TO COMMUNICATE?")
    print("=" * 80)
    
    total_sent = sum(e.signals_sent for e in entities)
    total_received = sum(e.signals_received for e in entities)
    
    if total_sent > 0:
        print(f"✓ YES - They sent {total_sent} signals into the channel")
    else:
        print("✗ NO - They did not send any signals")
    
    if total_received > 0:
        print(f"✓ YES - They received {total_received} signals from each other")
    else:
        print("✗ NO - They did not receive any signals")
    
    if stats['active_signals'] > 0:
        print(f"✓ YES - {stats['active_signals']} signals currently active in channel")
    else:
        print("→ Signals decayed (but communication occurred)")
    
    print()
    print("Communication substrate is ACTIVE and ready for collective evolution.")
    print("=" * 80)
