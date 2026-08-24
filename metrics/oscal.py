"""Express a metrics report in an OSCAL-shaped assessment-results object.

This is deliberately a *shape*, not a conformant OSCAL document: it uses OSCAL's
assessment-layer vocabulary (metadata / results / observations / findings) so the
payload can later be mapped onto the real model without reworking the service.
Identifiers are UUIDv5 values derived from the repository and metric name, so
the same input always produces the same document.
"""

import uuid
from typing import Any

from version import METRICS_VERSION

OSCAL_VERSION = "1.1.2"
NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/Andrewkadz/HARMONIA-DSL")


def _uuid(*parts: str) -> str:
    return str(uuid.uuid5(NAMESPACE, "/".join(parts)))


def _observation(
    report: dict[str, Any], name: str, description: str, value: Any
) -> dict[str, Any]:
    slug = f"{report['owner']}/{report['repo']}"
    return {
        "uuid": _uuid("observation", slug, name),
        "title": name,
        "description": description,
        "methods": ["TEST"],
        "collected": report["collected_at"],
        "props": [{"name": name, "value": str(value)}],
    }


def to_assessment_results(report: dict[str, Any]) -> dict[str, Any]:
    """Return ``report`` wrapped in an OSCAL-shaped assessment-results object."""
    slug = f"{report['owner']}/{report['repo']}"
    baseline = report["baseline"]
    ri1 = report["ri1"]

    observations = [
        _observation(
            report,
            "event_count",
            "GitHub events observed in the fetched window.",
            baseline["event_count"],
        ),
        _observation(
            report,
            "weekly_activity",
            "Event counts per calendar week (week-ending dates).",
            baseline["weekly_activity"],
        ),
        _observation(
            report,
            "harmonic_coherence_index",
            ri1["notes"],
            ri1["harmonic_coherence_index"],
        ),
    ]

    findings = []
    lever = ri1.get("recommended_lever")
    if lever:
        findings.append(
            {
                "uuid": _uuid("finding", slug, lever["name"]),
                "title": f"Out-of-band lever: {lever['name']}",
                "description": (
                    f"{lever['description']}. Current value "
                    f"{lever['current_value']} {lever['unit']} against a target of "
                    f"{lever['target_value']} {lever['unit']} "
                    f"(severity {lever['severity']}, n={lever['sample_size']})."
                ),
                "target": {
                    "type": "objective-id",
                    "target-id": lever["name"],
                    "status": {"state": "not-satisfied"},
                },
            }
        )

    return {
        "assessment-results": {
            "uuid": _uuid("assessment-results", slug, report["collected_at"]),
            "metadata": {
                "title": f"RI1 metrics assessment for {slug}",
                "last-modified": report["collected_at"],
                "version": METRICS_VERSION,
                "oscal-version": OSCAL_VERSION,
            },
            "import-ap": {"href": "#ri1-metrics-component-definition"},
            "results": [
                {
                    "uuid": _uuid("result", slug, report["collected_at"]),
                    "title": "GitHub activity assessment",
                    "description": (
                        "Deterministic baseline activity metrics and RI1 overlays "
                        "derived from the GitHub events, pulls, and issues APIs."
                    ),
                    "start": report["collected_at"],
                    "end": report["collected_at"],
                    "observations": observations,
                    "findings": findings,
                }
            ],
        },
        "ri1-payload": report,
    }
