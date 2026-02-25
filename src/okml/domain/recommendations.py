from __future__ import annotations

from okml.domain.models import AssessmentScores, LegacyEnvironment, RoadmapItem


def recommend(env: LegacyEnvironment, scores: AssessmentScores) -> list[RoadmapItem]:
    items: list[RoadmapItem] = []

    def add(
        *,
        id: str,
        title: str,
        rationale: str,
        effort: str,
        impact: str,
        risk_reduction: str,
        priority: int,
        tags: list[str],
    ) -> None:
        items.append(
            RoadmapItem(
                id=id,
                title=title,
                rationale=rationale,
                effort=effort,  # type: ignore[arg-type]
                impact=impact,  # type: ignore[arg-type]
                risk_reduction=risk_reduction,  # type: ignore[arg-type]
                priority=priority,
                tags=tags,
            )
        )

    if scores.reliability_risk >= 60 or not env.control_plane.ha_enabled:
        add(
            id="R-001",
            title="Harden OpenStack control plane (HA, clustered DB and message bus)",
            rationale=(
                "Reduce single points of failure and improve recovery behavior by standardizing "
                "HA patterns across controller services."
            ),
            effort="M",
            impact="H",
            risk_reduction="H",
            priority=1,
            tags=["openstack", "reliability", "control-plane"],
        )

    if env.config_drift_rate_percent >= 10 or scores.automation_maturity <= 45:
        add(
            id="A-010",
            title=(
                "Shift to automation-first provisioning (Terraform patterns + Ansible enforcement)"
            ),
            rationale=(
                "Lower error rate and cycle time by making provisioning deterministic, "
                "reviewable, and easier to validate."
            ),
            effort="M",
            impact="H",
            risk_reduction="H",
            priority=2,
            tags=["terraform", "ansible", "devops", "automation"],
        )

    add(
        id="K-020",
        title="Standardize Kubernetes baseline (namespaces, RBAC, policies, and release cadence)",
        rationale=(
            "Reduce operational variance and improve day-2 reliability with consistent "
            "cluster standards and upgrade practices."
        ),
        effort="M",
        impact="H",
        risk_reduction="M",
        priority=3,
        tags=["kubernetes", "standardization"],
    )

    add(
        id="O-030",
        title="Operationalize SLOs, runbooks, and change management gates",
        rationale=(
            "Sustain reliability gains by turning standards into daily practice "
            "(incident response, upgrades, backups, and capacity reviews)."
        ),
        effort="S",
        impact="H",
        risk_reduction="H",
        priority=4,
        tags=["operations", "sre", "governance"],
    )

    if env.network.east_west_visibility == "low":
        add(
            id="N-040",
            title=(
                "Improve east-west visibility and change safety "
                "(baseline telemetry + review workflow)"
            ),
            rationale=(
                "Lower change failure rate by tightening feedback loops and visibility "
                "for internal traffic and service dependencies."
            ),
            effort="S",
            impact="M",
            risk_reduction="M",
            priority=5,
            tags=["network", "observability"],
        )

    return sorted(items, key=lambda x: x.priority)
