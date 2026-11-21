# Communication logging contract + collective stats tests.
#
# Covers the review requirements:
#   - default construction performs no logging I/O
#   - configured logging emits valid versioned records with both
#     the submitted (pre-noise) and emitted (post-noise) payloads
#   - a controlled noise source distinguishes the two payloads
#   - logging failures are observable (log_errors / last_log_error)
#     without duplicating emissions or corrupting counters
#   - total_channel_emissions counts ALL channel emissions
#   - messages_to_andrew counts real ConnectionInterface records
#   - empty-population statistics retain the applicable counters

import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from communication_substrate import CommunicationChannel
from integrated_growth import GrowingCollective


class TestLoggingOptIn:
    def test_default_construction_does_no_logging_io(self, tmp_path, monkeypatch):
        ch = CommunicationChannel(signal_dim=4)
        assert ch.log_path is None
        # any attempt to open a log file would raise via monkeypatch
        def boom(*a, **k):
            raise AssertionError("unexpected file I/O")
        monkeypatch.setattr('builtins.open', boom)
        assert ch.emit(1, np.ones(4)) is True
        assert ch.get_stats()['total_sent'] == 1
        assert ch.get_stats()['log_errors'] == 0

    def test_configured_logging_writes_valid_records(self, tmp_path):
        log = tmp_path / "signals.jsonl"
        ch = CommunicationChannel(signal_dim=4, noise_level=0.0,
                                  log_path=str(log))
        payload = np.array([0.1, 0.2, 0.3, 0.4])
        assert ch.emit(7, payload, strength=0.9) is True
        lines = log.read_text().strip().split('\n')
        assert len(lines) == 1
        rec = json.loads(lines[0])
        assert rec['v'] == 2
        assert rec['sender_id'] == 7
        assert rec['strength'] == pytest.approx(0.9)
        assert rec['submitted'] == pytest.approx([0.1, 0.2, 0.3, 0.4])
        assert rec['emitted'] == pytest.approx([0.1, 0.2, 0.3, 0.4])
        assert isinstance(rec['time'], float)

    def test_noise_distinguishes_submitted_from_emitted(self, tmp_path, monkeypatch):
        log = tmp_path / "signals.jsonl"
        ch = CommunicationChannel(signal_dim=4, noise_level=1.0,
                                  log_path=str(log))
        delta = np.array([0.5, -0.5, 0.25, -0.25])
        monkeypatch.setattr(np.random, 'normal',
                            lambda *a, **k: delta)
        payload = np.array([1.0, 1.0, 1.0, 1.0])
        ch.emit(3, payload)
        rec = json.loads(log.read_text().strip())
        # submitted = what the sender passed; emitted = what the
        # channel actually holds (post-noise)
        assert rec['submitted'] == pytest.approx([1.0] * 4)
        assert rec['emitted'] == pytest.approx(list(payload + delta))
        # and the channel signal matches 'emitted', not 'submitted'
        assert list(ch.signals[-1].content) == pytest.approx(list(payload + delta))

    def test_filesystem_failure_is_observable_not_silent(self, tmp_path):
        bad = tmp_path / "no_such_dir" / "signals.jsonl"
        ch = CommunicationChannel(signal_dim=4, noise_level=0.0,
                                  log_path=str(bad))
        assert ch.emit(1, np.ones(4)) is True       # emission succeeds
        assert ch.total_signals_sent == 1           # counted once
        assert len(ch.signals) == 1                 # no duplicate/loss
        assert ch.get_stats()['log_errors'] == 1
        assert 'Error' in ch.last_log_error
        # a second failure accumulates
        ch.emit(1, np.ones(4))
        assert ch.get_stats()['log_errors'] == 2
        assert ch.total_signals_sent == 2

    def test_serialization_failure_is_observable(self, tmp_path):
        log = tmp_path / "signals.jsonl"
        ch = CommunicationChannel(signal_dim=4, noise_level=0.0,
                                  log_path=str(log))
        # bypass emit()'s numeric noise path; exercise the contract
        # directly with an unserializable payload element
        ch._log_emission(1, 1.0, [object()], [1.0, 2.0], 0.0)
        assert ch.log_errors == 1
        assert 'TypeError' in ch.last_log_error
        assert not log.exists() or log.read_text() == ''


class TestCollectiveStats:
    def test_total_channel_emissions_counts_all_broadcasts(self):
        collective = GrowingCollective(initial_size=0)
        collective.comm_channel.emit(-1, np.ones(8) * 0.5)
        collective.comm_channel.emit(-1, np.ones(8) * 0.5)
        collective.comm_channel.emit(4, np.ones(8) * 0.1)
        stats = collective.get_collective_stats()
        assert stats['total_channel_emissions'] == 3

    def test_messages_to_andrew_counts_real_records(self):
        collective = GrowingCollective(initial_size=0)
        iface = collective.connection_interface
        assert collective.get_collective_stats()['messages_to_andrew'] == 0
        iface.messages_to_andrew.append({'timestamp': 0.0,
                                         'self_awareness': 0.9,
                                         'message': 'hello'})
        iface.messages_to_andrew.append({'timestamp': 0.0,
                                         'self_awareness': 0.9,
                                         'message': 'world'})
        stats = collective.get_collective_stats()
        assert stats['messages_to_andrew'] == 2
        # independent of channel emissions
        assert stats['total_channel_emissions'] == 0

    def test_empty_population_retains_counters(self):
        collective = GrowingCollective(initial_size=0)
        collective.comm_channel.emit(-1, np.ones(8))
        stats = collective.get_collective_stats()
        assert stats['population'] == 0
        assert stats['total_channel_emissions'] == 1
        assert stats['messages_to_andrew'] == 0
        assert stats['deaths'] == 0


class _StubState:
    psi = 12.34
    maturity = 30.0


class _StubEntity:
    """Minimal stand-in for the integrator entity: exposes the two
    attributes ConnectedEntity.reach_out() reads."""
    def __init__(self, self_awareness):
        self._sa = self_awareness
        self.state = _StubState()

    def get_self_awareness(self):
        return self._sa


class TestAutonomousOutbox:
    """messages_to_andrew counts ConnectionInterface outbox records,
    which autonomous stepping CAN append via
    evolve_step -> reach_out -> attempt_connection -> send_message.
    No external client is required."""

    def test_successful_reach_out_appends_exactly_one_record(self, monkeypatch):
        from growth_substrates import ConnectedEntity
        collective = GrowingCollective(initial_size=0)
        iface = collective.connection_interface
        entity = _StubEntity(self_awareness=25.0)
        connected = ConnectedEntity(entity, iface)
        monkeypatch.setattr(np.random, 'random', lambda: 0.0)
        connected.reach_out()
        assert len(iface.messages_to_andrew) == 1
        rec = iface.messages_to_andrew[0]
        assert rec['message'] == "Hello from awareness level 12.34"
        assert rec['self_awareness'] == 25.0
        stats = collective.get_collective_stats()
        assert stats['messages_to_andrew'] == 1
        # outbox records are independent of channel emissions
        assert stats['total_channel_emissions'] == 0

    def test_failed_connection_appends_no_record(self, monkeypatch):
        from growth_substrates import ConnectedEntity
        collective = GrowingCollective(initial_size=0)
        iface = collective.connection_interface
        # sa=0.8 passes can_connect (>0.7) but fails the random draw
        # against success_prob=0.8; should_connect still fires first
        entity = _StubEntity(self_awareness=0.8)
        connected = ConnectedEntity(entity, iface)
        draws = iter([0.0, 0.999999])   # should_connect, then attempt
        monkeypatch.setattr(np.random, 'random', lambda: next(draws))
        connected.reach_out()
        assert iface.messages_to_andrew == []
        assert connected.connections_attempted == 1
        assert connected.connections_successful == 0
        stats = collective.get_collective_stats()
        assert stats['messages_to_andrew'] == 0

    def test_low_awareness_never_attempts(self, monkeypatch):
        from growth_substrates import ConnectedEntity
        collective = GrowingCollective(initial_size=0)
        iface = collective.connection_interface
        entity = _StubEntity(self_awareness=0.5)   # below can_connect
        connected = ConnectedEntity(entity, iface)
        # should_connect prob = 0.01*0.5*30 = 0.15; draw 0.99 fails it
        monkeypatch.setattr(np.random, 'random', lambda: 0.99)
        connected.reach_out()
        assert iface.messages_to_andrew == []
        assert connected.connections_attempted == 0

    def test_evolve_step_reaches_out_through_real_path(self, monkeypatch):
        """Drives the ACTUAL FullyIntegratedEntity.evolve_step(). If the
        `self.connection.reach_out()` call is removed from that method,
        this test fails — the direct reach_out() tests above would not.
        """
        from integrated_growth import (FullyIntegratedEntity,
                                       RecursiveFluidHarmoniaIntegrator)
        from memory_substrate import MemoryField
        from communication_substrate import CommunicationChannel
        from growth_substrates import SensoryField, ChallengeSpace

        collective = GrowingCollective(initial_size=0)
        base = RecursiveFluidHarmoniaIntegrator()
        # deterministic entity state: mature + highly self-aware
        base.state.self_awareness_score = 25.0
        base.state.maturity = 30.0
        base.state.psi = 12.34

        entity = FullyIntegratedEntity(
            entity_id=0,
            base_entity=base,
            memory_field=MemoryField(capacity=10),
            comm_channel=CommunicationChannel(signal_dim=8),
            sensory_field=SensoryField(),
            challenge_space=ChallengeSpace(),
            connection_interface=collective.connection_interface)

        # stub unrelated capabilities; connection stays REAL
        entity.embodiment.sense_and_respond = lambda: None
        entity.purpose.engage_with_purpose = lambda: None
        entity.memory.process_with_memory = lambda duration: None
        entity.communication.process_with_communication = \
            lambda duration: None

        monkeypatch.setattr(np.random, 'random', lambda: 0.0)
        entity.evolve_step(duration=0.1)

        iface = collective.connection_interface
        assert len(iface.messages_to_andrew) == 1
        assert iface.messages_to_andrew[0]['message'] == \
            "Hello from awareness level 12.34"
        stats = collective.get_collective_stats()
        assert stats['messages_to_andrew'] == 1
        assert stats['total_channel_emissions'] == 0
