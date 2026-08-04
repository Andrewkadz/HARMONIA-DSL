# Tests for the visualizer trace capture and HTML export.
#
# Additive observability only: per-round snapshots and the exporter
# must not perturb any swarm behavior (the full suite running green
# alongside these tests is itself the no-perturbation check).

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm_brain.baseline_swarm import BaselineSwarm
from swarm_brain.export_traces import build_html, collect_traces
from swarm_brain.governed_swarm import GovernedSwarm
from swarm_brain.task_spec import make_scenario


class TestPerRoundSnapshots:
    def test_snapshot_per_round_both_swarms(self):
        for cls in (BaselineSwarm, GovernedSwarm):
            trace = cls(make_scenario(), 60).run()
            assert len(trace.per_round) == trace.rounds_used
            assert [s["r"] for s in trace.per_round] == \
                list(range(1, trace.rounds_used + 1))

    def test_holdings_reference_real_resources_and_agents(self):
        s = make_scenario()
        trace = GovernedSwarm(s, 60).run()
        for snap in trace.per_round:
            for agent, resources in snap["hold"].items():
                assert 0 <= int(agent) < s.num_agents
                assert all(r in s.resources for r in resources)

    def test_events_carry_explanations(self):
        """Refusals and idles must carry human-readable 'why' strings —
        the teaching layer of the visualizer."""
        trace = GovernedSwarm(make_scenario(), 60).run()
        events = [e for snap in trace.per_round for e in snap["ev"]]
        refusals = [e for e in events if e["t"] == "refuse"]
        idles = [e for e in events if e["t"] == "idle"]
        assert refusals and all("why" in e for e in refusals)
        assert idles and all("why" in e for e in idles)

    def test_final_snapshot_matches_trace_totals(self):
        trace = GovernedSwarm(make_scenario(), 60).run()
        last = trace.per_round[-1]
        assert set(last["done"]) == trace.completed
        assert set(last["ref"]) == trace.refused


class TestExport:
    def test_collect_three_traces(self):
        meta, traces = collect_traces()
        labels = [t["label"] for t in traces]
        assert len(traces) == 3
        assert any("Baseline" in l for l in labels)
        assert any("stubbed" in l for l in labels)
        # the stubbed trace demonstrates G4 collapse in exported form:
        stubbed = next(t for t in traces if "stubbed" in t["label"])
        governed = next(t for t in traces if t["label"].startswith("Governed ("))
        assert set(governed["completed"]) == set(meta["tasks"]) - {"P"}
        assert set(stubbed["completed"]) != set(meta["tasks"]) - {"P"}

    def test_html_is_self_contained_with_embedded_data(self):
        meta, traces = collect_traces()
        html = build_html(meta, traces)
        assert html.startswith("<!DOCTYPE html>")
        assert "__DATA__" not in html and "__TITLE__" not in html
        # embedded JSON must be extractable and parseable
        start = html.index("const DATA = ") + len("const DATA = ")
        end = html.index(";\n", start)
        payload = json.loads(html[start:end])
        assert payload["meta"]["num_agents"] == 12
        assert len(payload["traces"]) == 3
