from __future__ import annotations

from okml.domain.kpis import generate_kpis
from okml.domain.models import LegacyEnvironment
from okml.domain.recommendations import recommend
from okml.domain.scoring import score_environment


def test_kpis_show_expected_improvement(sample_env: LegacyEnvironment) -> None:
    scores = score_environment(sample_env)
    recs = recommend(sample_env, scores)
    kpis = generate_kpis(scores=scores, recommendations=recs, seed=2026)
    assert kpis["after"]["uptime_monthly_percent"] >= 99.0
    assert (
        kpis["after"]["provisioning_time_minutes_p50"]
        < kpis["before"]["provisioning_time_minutes_p50"]
    )
