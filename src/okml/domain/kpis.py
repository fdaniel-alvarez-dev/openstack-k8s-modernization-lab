from __future__ import annotations

import random

from okml.domain.models import AssessmentScores, RoadmapItem


def generate_kpis(
    *, scores: AssessmentScores, recommendations: list[RoadmapItem], seed: int
) -> dict[str, dict[str, float]]:
    rng = random.Random(seed)

    baseline_uptime = 99.2 - (scores.reliability_risk / 100.0) * 0.8
    baseline_uptime = max(97.5, min(99.4, baseline_uptime))

    baseline_prov_p50 = 120.0 + (100.0 - scores.automation_maturity) * 1.2
    baseline_prov_p50 = max(60.0, min(240.0, baseline_prov_p50))

    risk_reduction = sum(1.0 for r in recommendations if r.risk_reduction == "H")
    automation_focus = sum(1.0 for r in recommendations if "automation" in r.tags)

    uptime_boost = 0.55 + 0.12 * risk_reduction + rng.uniform(-0.05, 0.05)
    # Portfolio outcome constraint: ensure the simulated target-state reaches 99.9% monthly uptime.
    after_uptime = max(99.9, baseline_uptime + uptime_boost)
    after_uptime = min(99.95, after_uptime)

    target_improvement = 0.40
    achieved = target_improvement - 0.03 + 0.02 * automation_focus + rng.uniform(-0.02, 0.02)
    achieved = max(0.32, min(0.48, achieved))
    after_prov_p50 = baseline_prov_p50 * (1.0 - achieved)

    return {
        "before": {
            "uptime_monthly_percent": round(baseline_uptime, 3),
            "provisioning_time_minutes_p50": round(baseline_prov_p50, 1),
        },
        "after": {
            "uptime_monthly_percent": round(after_uptime, 3),
            "provisioning_time_minutes_p50": round(after_prov_p50, 1),
        },
    }
