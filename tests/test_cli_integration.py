from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from okml.cli import app


def test_demo_generates_expected_artifacts(tmp_path: Path) -> None:
    runner = CliRunner()
    artifacts_dir = tmp_path / "artifacts"
    result = runner.invoke(
        app,
        ["demo", "--artifacts-dir", str(artifacts_dir), "--seed", "2026", "--log-format", "json"],
    )
    assert result.exit_code == 0, result.stdout

    assert (artifacts_dir / "assessment" / "assessment_report.md").exists()
    assert (artifacts_dir / "design" / "architecture.mmd").exists()
    assert (artifacts_dir / "automation" / "terraform_outputs.json").exists()
    assert (artifacts_dir / "kpis" / "dashboard.html").exists()
    assert (artifacts_dir / "executive" / "executive_summary.md").exists()

    kpis = json.loads((artifacts_dir / "kpis" / "kpis.json").read_text(encoding="utf-8"))
    assert kpis["after"]["uptime_monthly_percent"] >= 99.9
