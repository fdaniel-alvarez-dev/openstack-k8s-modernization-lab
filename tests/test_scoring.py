from __future__ import annotations

from okml.domain.models import LegacyEnvironment
from okml.domain.scoring import score_environment


def test_score_environment_is_deterministic(sample_env: LegacyEnvironment) -> None:
    s1 = score_environment(sample_env)
    s2 = score_environment(sample_env)
    assert s1 == s2
    assert 0 <= s1.reliability_risk <= 100
    assert 0 <= s1.operational_maturity <= 100
    assert 0 <= s1.automation_maturity <= 100
    assert 0 <= s1.standardization <= 100
