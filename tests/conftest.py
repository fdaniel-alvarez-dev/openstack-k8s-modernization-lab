from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from okml.domain.models import LegacyEnvironment


@pytest.fixture()
def sample_env() -> LegacyEnvironment:
    data = yaml.safe_load(Path("sample_data/legacy_env.yaml").read_text(encoding="utf-8"))
    return LegacyEnvironment.model_validate(data)
