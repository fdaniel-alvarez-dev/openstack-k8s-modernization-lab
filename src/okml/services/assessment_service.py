from __future__ import annotations

import json
from pathlib import Path

import yaml

from okml.config import Settings
from okml.domain.models import AssessmentReport, AssessmentScores, LegacyEnvironment
from okml.domain.recommendations import recommend
from okml.domain.scoring import score_environment
from okml.reporting.writers import (
    render_assessment_md,
    write_json,
    write_risk_register_csv,
    write_text,
)
from okml.utils.fs import ensure_dir
from okml.utils.logging import get_logger


class AssessmentService:
    def __init__(self, *, settings: Settings, run_id: str) -> None:
        self._settings = settings
        self._run_id = run_id
        self._log = get_logger(__name__)

    def run(self, *, input_path: Path) -> AssessmentReport:
        env = self._load_env(input_path)
        scores = score_environment(env)
        recs = recommend(env, scores)

        findings = self._derive_findings(env, scores)
        report = AssessmentReport(env=env, scores=scores, findings=findings, recommendations=recs)

        out_dir = ensure_dir(self._settings.artifacts_dir / "assessment")
        write_text(out_dir / "assessment_report.md", render_assessment_md(report))
        write_json(out_dir / "assessment_report.json", json.loads(report.model_dump_json()))
        write_risk_register_csv(out_dir / "risk_register.csv", recs)

        self._log.info(
            "assessment_complete",
            extra={"run_id": self._run_id, "out_dir": str(out_dir), "env": env.name},
        )
        return report

    def _load_env(self, input_path: Path) -> LegacyEnvironment:
        raw = input_path.read_text(encoding="utf-8")
        if input_path.suffix.lower() in {".yaml", ".yml"}:
            data = yaml.safe_load(raw)
        else:
            data = json.loads(raw)
        return LegacyEnvironment.model_validate(data)

    def _derive_findings(self, env: LegacyEnvironment, scores: AssessmentScores) -> list[str]:
        findings: list[str] = []
        total_prov = sum(s.minutes_p50 for s in env.provisioning_workflow)
        manual = sum(s.manual_touchpoints for s in env.provisioning_workflow)
        findings.append(
            f"Provisioning workflow P50 is ~{round(total_prov, 1)} minutes "
            f"with {manual} manual touchpoints."
        )
        if not env.control_plane.ha_enabled:
            findings.append(
                "Control plane HA is not enabled; reliability risk increases during "
                "upgrades and failures."
            )
        if env.config_drift_rate_percent >= 10:
            findings.append(
                f"Config drift rate is {env.config_drift_rate_percent}%, "
                "indicating inconsistent operations."
            )
        if scores.automation_maturity <= 45:
            findings.append(
                "Automation maturity is low; inconsistent provisioning and "
                "manual changes drive variance."
            )
        if env.network.east_west_visibility == "low":
            findings.append(
                "East-west visibility is low; change impact is harder to predict and validate."
            )
        return findings
