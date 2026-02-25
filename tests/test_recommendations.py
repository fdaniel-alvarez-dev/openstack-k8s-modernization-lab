from __future__ import annotations

from okml.domain.models import LegacyEnvironment
from okml.domain.recommendations import recommend
from okml.domain.scoring import score_environment


def test_recommendations_prioritized(sample_env: LegacyEnvironment) -> None:
    scores = score_environment(sample_env)
    recs = recommend(sample_env, scores)
    assert len(recs) >= 3
    priorities = [r.priority for r in recs]
    assert priorities == sorted(priorities)
